/*
File: ServiceConsole.java ; This file is part of Twister.
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
import java.awt.Color;
import java.awt.Component;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.FileInputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Properties;

import javax.swing.JCheckBox;
import javax.swing.JDesktopPane;
import javax.swing.JInternalFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.event.InternalFrameAdapter;
import javax.swing.event.InternalFrameEvent;

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.twister.Item;
import com.twister.plugin.baseplugin.BasePlugin;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.w3c.dom.Document;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Result;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.bind.DatatypeConverter;

public class ServiceConsole extends BasePlugin implements TwisterPluginInterface {
	private static final long serialVersionUID = 1L;
	private JPanel p;
	private ChannelSftp c;
	private XmlRpcClient client;
	private JCheckBox [] services;

	@Override
	public void init(ArrayList <Item>suite,ArrayList <Item>suitetest,
			  final Hashtable<String, String>variables,
			  Document pluginsConfig,Applet container){
		super.init(suite, suitetest, variables,pluginsConfig,container);
		System.out.println("Initializing " + getName() + " ... ");
		//initializeSFTP();
		initializeRPC();
		//createXMLStructure();
		
		JMenuBar menubar = new JMenuBar();
		JMenu menu = new JMenu("Services");
		menubar.add(menu);
		
		final JDesktopPane pane = new JDesktopPane();
		
		p = new JPanel();
		p.setLayout(new BorderLayout());
		
		p.add(menubar,BorderLayout.NORTH);
		p.add(pane,BorderLayout.CENTER);
		
		String [] serv = getServices();
		services = new JCheckBox[serv.length];
		for(int i=0;i<serv.length;i++){
			services[i] = new JCheckBox(serv[i]);
			services[i].addActionListener(new ActionListener() {
				@Override
				public void actionPerformed(ActionEvent arg0) {
					if(((JCheckBox)arg0.getSource()).isSelected()){
						MyInternalFrame frame = new MyInternalFrame(((JCheckBox)arg0.getSource()).getText());
						pane.add(frame);
						frame.setLocation(50, 10);
						frame.setSize(300, 200);
						frame.setVisible(true);
					} else {
						for(JInternalFrame f:pane.getAllFrames()){
							if(f.getTitle().equals(((JCheckBox)arg0.getSource()).getText())){
								f.dispose();
								break;
							}
						}
					}
				}
			});
			menu.add(services[i]);
		}
		System.out.println(getName() + " initialized");
	}
	
	private String [] getServices(){
		String result;
		try {
			result = client.execute("serviceManagerCommand",
			        new Object[]{"list"}).toString();
			return result.split(",");       
		} catch (XmlRpcException e) {
			e.printStackTrace();
			return null;
		}	
	}

	@Override
	public Component getContent() {
		return p;
	}

	@Override
	public String getFileName() {
		String filename = "ServiceConsole.jar";
		return filename;
	}

	@Override
	public void terminate() {
		super.terminate();
		p = null;
		client = null;
		services = null;
	}

	@Override
	public String getName(){
		String name = "ServiceConsole";
		return name;
	}

//	public void initializeSFTP() {
//		try {
//			JSch jsch = new JSch();
//			String user = variables.get("user");
//			Session session = jsch.getSession(user, variables.get("host"), 22);
//			session.setPassword(variables.get("password"));
//			Properties config = new Properties();
//			config.put("StrictHostKeyChecking", "no");
//			session.setConfig(config);
//			session.connect();
//			Channel channel = session.openChannel("sftp");
//			channel.connect();
//			c = (ChannelSftp) channel;
//			System.out.println("SFTP successfully initialized");
//		} catch (Exception e) {
//			System.out.println("SFTP could not be initialized");
//			e.printStackTrace();
//		}
//	}

	public void initializeRPC() {
		try {
			XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
			configuration.setServerURL(new URL("http://"
					+ variables.get("host") + ":"
					+ variables.get("centralengineport")));
			configuration.setBasicPassword(variables.get("password"));
            configuration.setBasicUserName(variables.get("user"));
			client = new XmlRpcClient();
			client.setConfig(configuration);
			System.out.println("Client initialized: " + client);
		} catch (Exception e) {
			System.out.println("Could not conect to " + variables.get("host")
					+ " :" + variables.get("centralengineport")
					+ "for RPC client initialization");
		}
	}

//	/*
//	 * method to copy plugins configuration file to server
//	 */
//	public boolean uploadPluginsFile() {
//		try {
//			DOMSource source = new DOMSource(pluginsConfig);
//			File file = new File(variables.get("pluginslocalgeneralconf"));
//			Result result = new StreamResult(file);
//			TransformerFactory transformerFactory = TransformerFactory
//					.newInstance();
//			Transformer transformer = transformerFactory.newTransformer();
//			transformer.setOutputProperty(OutputKeys.INDENT, "yes");
//			transformer.setOutputProperty(
//					"{http:xml.apache.org/xslt}indent-amount", "4");
//			transformer.transform(source, result);
//			FileInputStream in = new FileInputStream(file);
//			String location =variables.get("remoteuserhome") + "/twister/config/"; 
//			c.cd(location);
//			c.put(in, file.getName());
//			in.close();
//			System.out.println("Saved " + file.getName() + " to: "
//					+ variables.get("remoteuserhome") + "/twister/config/");
//			return true;
//		} catch (Exception e) {
//			e.printStackTrace();
//			return false;
//		}
//	}
	
	class MyInternalFrame extends JInternalFrame{
		private static final long serialVersionUID = 1L;
		private boolean run;
		private JTextArea text;
		private long lastindex = 0;
		
		public MyInternalFrame(String title){
			super(title,true, true, true, true);
			text = new JTextArea();
			text.setEditable(false);
			text.setBackground(Color.BLACK);
			text.setForeground(Color.WHITE);
			text.setFont(new Font("Monospaced",Font.PLAIN, 12));
			JScrollPane sc = new JScrollPane(text);
			add(sc);
			addInternalFrameListener(new InternalFrameAdapter(){
				public void internalFrameClosing(InternalFrameEvent e) {
					for(JCheckBox check:services){
						if(check.getText().equals(getTitle())){
							check.setSelected(false);
							run = false;
							dispose();
						}
					}
			    }
			});
			run	= true;
			new Thread(){
				public void run(){
					while(run){
						if(p.isVisible())getLog();
						try{Thread.sleep(1000);}
						catch(Exception e){e.printStackTrace();}
					}
				}
				
			}.start();
		}
		
		
		public void getLog(){
			try {
				String result = client.execute("serviceManagerCommand",
				        new Object[]{"get log",getTitle(),0,0}).toString();
				long curentpos = Long.parseLong(result);
				if(curentpos>lastindex){
					result = client.execute("serviceManagerCommand",
					        new Object[]{"get log",getTitle(),1,lastindex+""}).toString();
					lastindex = curentpos;
			        byte mydata[]=null;
			        try{mydata = DatatypeConverter.parseBase64Binary(result);}
			        catch(Exception e){e.printStackTrace();}
					text.append(new String(mydata));
				} else if(curentpos<lastindex){
					result = client.execute("serviceManagerCommand",
					        new Object[]{"get log",getTitle(),1,0}).toString();
					lastindex = curentpos;
					byte mydata[]=null;
			        try{mydata = DatatypeConverter.parseBase64Binary(result);}
			        catch(Exception e){e.printStackTrace();}
					text.setText(new String(mydata));
				}
			} catch (XmlRpcException e) {
				e.printStackTrace();
			}
		}
	}
}
