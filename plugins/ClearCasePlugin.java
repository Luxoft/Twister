/*
File: ClearCasePlugin.java ; This file is part of Twister.
Version: 2.001

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
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;

import javax.swing.BorderFactory;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.border.Border;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.twister.Item;
import com.twister.plugin.baseplugin.BasePlugin;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.w3c.dom.Document;

public class ClearCasePlugin extends BasePlugin implements TwisterPluginInterface {
	private static final long serialVersionUID = 1L;    
	private JPanel p;
	private XmlRpcClient client;

	@Override
	public void init(ArrayList <Item>suite,ArrayList <Item>suitetest,
			  final Hashtable<String, String>variables,
			  Document pluginsConfig,Applet container){
		super.init(suite, suitetest, variables,pluginsConfig,container);
		System.out.println("Initializing "+getName()+" ...");
//		initializeSFTP();
		initializeRPC();
		p = new JPanel();
		p.setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
		p.setBackground(Color.black);
		p.setLayout(new BorderLayout());
		final JTextField tf = new JTextField();
		final JTextArea ta = new JTextArea();
		ta.setBackground(Color.black);
		ta.setForeground(Color.WHITE);
		ta.setFont(new Font("Monospaced",Font.PLAIN, 12));
		ta.setEditable(false);
		ta.addFocusListener(new FocusAdapter() {
			public void focusGained(FocusEvent ev){
				tf.requestFocus();
			}
		});
		
		tf.setCaretColor(Color.white);
		tf.setBorder(null);
		tf.setBackground(Color.black);
		tf.setForeground(Color.WHITE);
		tf.setFont(new Font("Monospaced",Font.PLAIN, 12));
		tf.addKeyListener(new KeyAdapter() {
			public void keyReleased(KeyEvent ev){
				if(ev.getKeyCode()==KeyEvent.VK_ENTER){
					String command = tf.getText();
					ta.append("command: "+command+"\n");
					String resp = executeCommand(command);
					JsonElement el = new JsonParser().parse(resp);
					JsonObject jobject = el.getAsJsonObject();
					String stat = jobject.get("status").getAsString();
					String data = jobject.get("data").getAsString();
					String err = jobject.get("error").getAsString();
					ta.append("error: "+err+"\n");
					ta.append("executed: "+stat.equals("0")+"\n");
					ta.append("respons: \n");
					ta.append(data+"\n");
					tf.setText("");
					ta.setCaretPosition(ta.getDocument().getLength());
				}
			}
		});
		JScrollPane sp = new JScrollPane(ta);
		sp.setBorder(null);
		p.add(sp, BorderLayout.CENTER);
		p.add(tf, BorderLayout.SOUTH);
//      createXMLStructure();
		System.out.println(getName()+" initialized");
//		executeCommand("lsvob");
	}

	@Override
	public Component getContent() {
		return p;
	}

	@Override
	public String getFileName() {
		String filename = "ClearCasePlugin.jar";
		return filename;
	}

	@Override
	public void terminate() {
		super.terminate();
//		c = null;
		p = null;
	}

	@Override
	public String getName() {
		String name = "ClearCase";
		return name;
	}
	
	public String executeCommand(String command){
		try {
			HashMap<String,String> commanddict = new HashMap<String,String>();
			commanddict.put("command", command);
			return client.execute("runPlugin", new Object[]{variables.get("user"),
					getName(), commanddict}).toString();
		} catch (XmlRpcException e) {
			System.out.println("Could not send command");
			e.printStackTrace();
			return e.getMessage();
		}
	}
	
//	public void initializeSFTP(){
//		try{
//			JSch jsch = new JSch();
//            String user = variables.get("user");
//            Session session = jsch.getSession(user, variables.get("host"), 22);
//            session.setPassword(variables.get("password"));
//            Properties config = new Properties();
//            config.put("StrictHostKeyChecking", "no");
//            session.setConfig(config);
//            session.connect();
//            Channel channel = session.openChannel("sftp");
//            channel.connect();
//            c = (ChannelSftp)channel;
//            System.out.println("SFTP successfully initialized");
//		}
//		catch(Exception e){
//			System.out.println("SFTP could not be initialized");
//			e.printStackTrace();
//		}
//	}
	
	public void initializeRPC(){
		try{XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
        configuration.setServerURL(new URL("http://"+variables.get("host")+
                                    ":"+variables.get("centralengineport")));
        configuration.setBasicPassword(variables.get("password"));
        configuration.setBasicUserName(variables.get("user"));
        client = new XmlRpcClient();
        client.setConfig(configuration);
        System.out.println("Client initialized: "+client);}
    catch(Exception e){System.out.println("Could not conect to "+
                        variables.get("host")+" :"+variables.get("centralengineport")+
                        "for RPC client initialization");}
	}
	
	/*
     * method to copy plugins configuration file
     * to server 
     */
//    public boolean uploadPluginsFile(){
//        try{
//            DOMSource source = new DOMSource(pluginsConfig);
//            File file = new File(variables.get("pluginslocalgeneralconf"));
//            Result result = new StreamResult(file);
//            TransformerFactory transformerFactory = TransformerFactory.newInstance();
//            Transformer transformer = transformerFactory.newTransformer();
//            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
//            transformer.setOutputProperty("{http:xml.apache.org/xslt}indent-amount","4");
//            transformer.transform(source, result);
//            c.cd(variables.get("remoteuserhome")+"/twister/config/");
//            FileInputStream in = new FileInputStream(file);
//            c.put(in, file.getName());
//            in.close();
//            System.out.println("Saved "+file.getName()+" to: "+
//					variables.get("remoteuserhome")+"/twister/config/");
//            return true;}
//        catch(Exception e){
//            e.printStackTrace();
//            return false;
//        }
//    }
	
	public static void main(String[] args) {
		try {
			ClearCasePlugin sch = new ClearCasePlugin();			
			Hashtable<String,String> hm = new Hashtable<String,String>();
			hm.put("host", "11.126.32.21");
			hm.put("user", "user");
			hm.put("password", "password");
			hm.put("centralengineport", "8000");
			sch.init(null,null,hm,  null,null);
			JFrame f = new JFrame();
			f.add(sch.getContent());
			f.setVisible(true);
			f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			f.setBounds(100, 50, 900, 900);
		} catch (Exception e) {
			System.out.println("Could not conect to "
					+ "http://tsc-server:8000 for RPC client initialization");
			e.printStackTrace();
		}
	}
	
}
