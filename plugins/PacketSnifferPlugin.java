/*
File: PacketSnifferPlugin.java ; This file is part of Twister.
Version: 2.002

Copyright (C) 2012-2013 , Luxoft

Authors: Andrei Costachi <acostachi@luxoft.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

import java.applet.Applet;
import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.Hashtable;

import javax.swing.DefaultListModel;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTextArea;
import javax.swing.ListSelectionModel;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.xml.bind.DatatypeConverter;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.twister.CustomDialog;
import com.twister.Item;
import com.twister.plugin.baseplugin.BasePlugin;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.w3c.dom.Document;

public class PacketSnifferPlugin extends BasePlugin implements TwisterPluginInterface,ActionListener {
	private static final long serialVersionUID = 1L;
	private XmlRpcClient client;
	private JPanel main_panel;
	private JList filelist;
	private DefaultListModel packets_summary_model,packets_detail_model;
	private JList packets_summary_list;
	private JPanel sniffer_panel;;
	private JTextArea tshark_view;
	private DefaultListModel filelist_model;

	@Override
	public void init(ArrayList <Item>suite,ArrayList <Item>suitetest,
			  final Hashtable<String, String>variables,
			  Document pluginsConfig,Applet container){
		try{super.init(suite, suitetest, variables,pluginsConfig,container);}
		catch(Exception e){e.printStackTrace();}
		System.out.println("Initializing "+getName()+" ...");
		initializeRPC();
		main_panel = new JPanel();
        main_panel.setLayout(new BorderLayout()); 
        initComponents();
		System.out.println(getName()+" initialized");
	}
	
	private void initComponents(){
		JButton deleteall = new JButton("Delete all files");
		JButton downloadfile = new JButton("Download file");
		JButton getfilelist = new JButton("List files");
		JButton deletefiles = new JButton("Delete file");
        deletefiles.setActionCommand("tshark_delete_files");
        deletefiles.addActionListener(this);
        getfilelist.addActionListener(this);
        getfilelist.setActionCommand("tshark_getfilelist");
        downloadfile.setActionCommand("tshark_download_file");
        downloadfile.addActionListener(this);
		deleteall.setActionCommand("tshark_delete_all_files");
        deleteall.addActionListener(this);
		tshark_view = new JTextArea();
		JScrollPane tshark_sp = new JScrollPane(tshark_view);
		packets_detail_model = new DefaultListModel();
		packets_summary_model = new DefaultListModel();
		packets_summary_list = new JList(packets_summary_model);
        packets_summary_list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        packets_summary_list.setSelectedIndex(0);        
        packets_summary_list.setVisibleRowCount(10);
        JScrollPane packets_summary_sp = new JScrollPane(packets_summary_list);
        packets_summary_list.addListSelectionListener(new ListSelectionListener() {
            public void valueChanged(ListSelectionEvent le) 
            {
                int idx = packets_summary_list.getSelectedIndex();
                if (idx != -1)
                {
                    tshark_view.setText(packets_detail_model.get(idx).toString());
                }
            }
        });
        packets_summary_sp.repaint();
		filelist_model = new DefaultListModel();
		filelist = new JList(filelist_model);
        filelist.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent evt) {
                JList list = (JList)evt.getSource();
                if (evt.getClickCount() == 2) {
                    int index = list.locationToIndex(evt.getPoint());
                    getPackets(((DefaultListModel)filelist.getModel()).get(index).toString());
                }
            }
        });
        filelist.setSelectionMode(ListSelectionModel.MULTIPLE_INTERVAL_SELECTION);
        filelist.setSelectedIndex(0);        
        filelist.setVisibleRowCount(10);
		JScrollPane filelist_sp= new JScrollPane(filelist);
		JPanel fileslist_panel = new JPanel();
        fileslist_panel.setLayout(new BorderLayout());
        fileslist_panel.add(filelist_sp, BorderLayout.CENTER);
        JPanel fileslist_buttons = new JPanel();
        fileslist_panel.add(fileslist_buttons, BorderLayout.SOUTH);
        fileslist_buttons.add(downloadfile);
        fileslist_buttons.add(getfilelist);
        fileslist_buttons.add(deletefiles);
        fileslist_buttons.add(deleteall);
		JSplitPane spv = new JSplitPane();
        spv.setOrientation(JSplitPane.HORIZONTAL_SPLIT);
        spv.setLeftComponent(fileslist_panel);
        spv.setRightComponent(packets_summary_sp);
        sniffer_panel = new JPanel(new BorderLayout());
		sniffer_panel.add(spv,BorderLayout.CENTER);
		
		JSplitPane sph = new JSplitPane();
        sph.setOrientation(JSplitPane.VERTICAL_SPLIT);
        sph.setLeftComponent(sniffer_panel);
        sph.setRightComponent(tshark_sp);
        main_panel.add(sph);
    }
	
	private void getPackets(String sv){
        if(sv!=null)
        {      
            String rs=tsharkRunCommand("tshark_getpackets",sv);
            fillTSharkPackets(rs);
        }
    }
	
	public String tsharkRunCommand(String c,String fname)
    {
        String cmd="command="+c;               
        cmd+="&cap_file="+fname;               
        try
        {                    
            String result = client.execute("run_plugin", 
                                new Object[]{variables.get("user"), getName(),cmd})+"";
            return result;                                            
        }
        catch (Exception e) 
        {
            e.printStackTrace();             
        }
        return "";         
    }
	
	public void fillTSharkPackets(String str)
    {
		if(showErrorMessage(str))return;
        packets_summary_model.clear();
        packets_detail_model.clear();
        try
        {
        	JsonElement json = new JsonParser().parse(str);
            JsonObject inifile = json.getAsJsonObject();
            JsonObject packets = inifile.get("tshark_getpackets").getAsJsonObject();
            JsonArray summary = packets.get("tshark_packets_summary").getAsJsonArray();
            JsonArray detail = packets.get("tshark_packets_detail").getAsJsonArray();            
            
            for(JsonElement el:summary)
            {
                packets_summary_model.addElement(el.getAsString());                                
            }
            
            for(JsonElement el:detail)
            {
                packets_detail_model.addElement(el.getAsString());                                
            }
        } 
        catch(Exception e){e.printStackTrace();}        
    }

	@Override
	public Component getContent() {
		return main_panel;
	}

	@Override
	public String getFileName() {
		String filename = "PacketSnifferPlugin.jar";
		return filename;
	}

	@Override
	public void terminate() {
		super.terminate();
		main_panel = null;
	}

	@Override
	public String getName() {
		String name = "PacketSnifferPlugin";
		return name;
	}
	
	public void initializeRPC(){
		try{XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
        configuration.setServerURL(new URL("http://"+variables.get("host")+
                                    ":"+variables.get("centralengineport")));
        configuration.setBasicPassword(variables.get("password"));
        configuration.setBasicUserName(variables.get("user"));
        client = new XmlRpcClient();
        client.setConfig(configuration);
        System.out.println("Client initialized: "+client);}
    catch(Exception e){System.out.println("Plugin"+getName()+"could not conect to XMLRPC server");}
	}
	
	
	public void actionPerformed(ActionEvent e) {
        if (e.getActionCommand().equals("tshark_download_file")) 
        {   
        	downloadFile();
        } else if (e.getActionCommand().equals("tshark_getfilelist")) 
        {   
        	String rs=tsharkRunCommand("tshark_getfilelist","");   
            fillTSharkFileList(rs);
        } else if (e.getActionCommand().equals("tshark_delete_files")) 
        {   
        	deleteFiles();
        } else if (e.getActionCommand().equals("tshark_delete_all_files")) 
        {   
        	deleteAllFiles();
        } 
    }
	
	private void deleteAllFiles(){
        String rs=tsharkRunCommand("tshark_delete_all_files","");
        if(showErrorMessage(rs))return;
        rs=tsharkRunCommand("tshark_getfilelist","");
        fillTSharkFileList(rs);           
    }
	
	private void deleteFiles(){
        int [] indices = filelist.getSelectedIndices();
        StringBuilder sb = new StringBuilder();
        for(int i=0;i<indices.length;i++){
            sb.append(((DefaultListModel)filelist.getModel()).get(indices[i]).toString());
            sb.append(",");
        }
        sb.setLength(sb.length()-1);
        String list = sb.toString();
        String rs=tsharkRunCommand("tshark_delete_files",list);
        if(showErrorMessage(rs))return;
        rs=tsharkRunCommand("tshark_getfilelist","");   
        if(showErrorMessage(rs))return;
        fillTSharkFileList(rs);           
    }
	
	public void fillTSharkFileList(String str)
    {
		if(showErrorMessage(str))return;
        filelist_model.clear();
        JsonElement jelement = new JsonParser().parse(str);
        JsonObject inifile = jelement.getAsJsonObject();
        JsonArray flist = inifile.getAsJsonArray("tshark_getfilelist");
        for(JsonElement el:flist)
        {            
            filelist_model.addElement(el.getAsString());
        }
        tshark_view.setText(str);        
    }
	
	private void downloadFile()
    {       

        int [] indices = filelist.getSelectedIndices();
        if(indices.length!=1){
            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, main_panel, "Error", "Please select one file");
            return;
        }
        String filenametodownload = ((DefaultListModel)filelist.getModel()).get(indices[0]).toString();
        JFileChooser chooser = new JFileChooser(); 
        chooser.setSelectedFile(new java.io.File(filenametodownload));
        chooser.setApproveButtonText("Save");
        chooser.setDialogTitle("Choose Location");         
        chooser.setAcceptAllFileFilterUsed(false);    
        if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) 
        {
            File downloadto = chooser.getSelectedFile();        
            try
            {
                byte [] buf = null;
                String rs=tsharkRunCommand("tshark_download_file",filenametodownload);  
                if(showErrorMessage(rs))return;
                buf=DatatypeConverter.parseBase64Binary(rs); 
                OutputStream out=new FileOutputStream(downloadto);
                out.write(buf);
                out.flush();
                out.close();
                System.out.println("successfull");
            } catch (Exception e){
                System.out.println("Could not download file "+filenametodownload);
                e.printStackTrace();
            }
        }
    }
	
	public boolean showErrorMessage(String error){
		if(error.contains("*ERROR*")){
			CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE, main_panel, "Error", error);
			return true;
		}
		return false;
	}
	
	public static void main(String [] args){
		Hashtable<String, String>variables = new Hashtable<String, String>();
		variables.put("password", "tscguest");
		variables.put("user", "tscguest");
		variables.put("centralengineport", "8000");
		variables.put("host", "11.126.32.9");
		JFrame frame = new JFrame();
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		PacketSnifferPlugin sp = new PacketSnifferPlugin();
		sp.init(null, null, variables, null, null);
		frame.add(sp.getContent());
		frame.setVisible(true);
	}
}