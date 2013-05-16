/*
File: JenkinsPlugin.java ; This file is part of Twister.
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

import java.awt.Component;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Properties;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.twister.Item;
import com.twister.MySftpBrowser;
import com.twister.plugin.baseplugin.BasePlugin;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.w3c.dom.Document;
import org.w3c.dom.Node;

import javax.xml.transform.OutputKeys;
import javax.xml.transform.Result;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

public class JenkinsPlugin extends BasePlugin implements TwisterPluginInterface {
	private static final long serialVersionUID = 1L;    
	private JPanel p;
	private XmlRpcClient client;
	private ChannelSftp c;
	private Node script, project;
	private JTextField tscript,tproject; 

	@Override
	public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
			final Hashtable<String, String> variables,final Document pluginsConfig) {
		super.init(suite, suitetest, variables,pluginsConfig);
		System.out.println("Initializing "+getName()+" ...");
		initializeSFTP();
		initializeRPC();
		p = new JPanel();
        createXMLStructure();
        script = getPropValue("script");
        project = getPropValue("project");
        JPanel panel = new JPanel();
        panel.setLayout(null);
        panel.setPreferredSize(new Dimension(300, 70));
        panel.setMinimumSize(new Dimension(300, 70));
        panel.setMaximumSize(new Dimension(300, 70));
        panel.setSize(300, 70);
        JLabel lscript = new JLabel("Script:");
        lscript.setBounds(5,5,60,25);
        panel.add(lscript);
        tscript = new JTextField();
        tscript.setBounds(70,5,150,25);
        tscript.setText(script.getNodeValue());
        panel.add(tscript);
        tscript.getDocument().addDocumentListener( new DocumentListener() {
			@Override
			public void removeUpdate(DocumentEvent e) {
				script.setNodeValue(tscript.getText());  
				uploadPluginsFile();
			}
			
			@Override
			public void insertUpdate(DocumentEvent e) {
				script.setNodeValue(tscript.getText());  
				uploadPluginsFile();
			}
			
			@Override
			public void changedUpdate(DocumentEvent e) {
				script.setNodeValue(tscript.getText());  
				uploadPluginsFile();
			}
		});
        JButton bscript = new JButton("...");
        bscript.setBounds(230,5,60,25);
        panel.add(bscript);
        bscript.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				//Repository.host,Repository.user,Repository.password,textfield,c
				MySftpBrowser browser = new MySftpBrowser(variables.get("host"), variables.get("user"), variables.get("password"), tscript, p);
				//MySftpBrowser browser = new MySftpBrowser(c, tscript, p);
			}
		});
        
        JLabel lproject = new JLabel("Project:");
        lproject.setBounds(5,35,60,25);
        panel.add(lproject);
        tproject = new JTextField();
        tproject.setBounds(70,35,150,25);
        tproject.setText(project.getNodeValue());
        panel.add(tproject);
        tproject.getDocument().addDocumentListener( new DocumentListener() {
			@Override
			public void removeUpdate(DocumentEvent e) {
				project.setNodeValue(tproject.getText());  
				uploadPluginsFile();
			}
			
			@Override
			public void insertUpdate(DocumentEvent e) {
				project.setNodeValue(tproject.getText());  
				uploadPluginsFile();
			}
			
			@Override
			public void changedUpdate(DocumentEvent e) {
				project.setNodeValue(tproject.getText());  
				uploadPluginsFile();
			}
		});
        JButton bproject = new JButton("...");
        bproject.setBounds(230,35,60,25);
        panel.add(bproject);
        bproject.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				MySftpBrowser browser = new MySftpBrowser(variables.get("host"), variables.get("user"), variables.get("password"), tproject, p);
				//MySftpBrowser browser = new MySftpBrowser(c, tproject, p);
			}
		});
        p.add(panel);
		System.out.println(getName()+" initialized");
	}

	@Override
	public Component getContent() {
		return p;
	}

	@Override
	public String getFileName() {
		String filename = "JenkinsPlugin.jar";
		return filename;
	}

	@Override
	public void terminate() {
		super.terminate();
		c = null;
		p = null;
	}

	@Override
	public String getName() {
		String name = "JenkinsPlugin";
		return name;
	}
	
	public void initializeSFTP(){
		try{
			JSch jsch = new JSch();
            String user = variables.get("user");
            Session session = jsch.getSession(user, variables.get("host"), 22);
            session.setPassword(variables.get("password"));
            Properties config = new Properties();
            config.put("StrictHostKeyChecking", "no");
            session.setConfig(config);
            session.connect();
            Channel channel = session.openChannel("sftp");
            channel.connect();
            c = (ChannelSftp)channel;
            System.out.println("SFTP successfully initialized");
		}
		catch(Exception e){
			System.out.println("SFTP could not be initialized");
			e.printStackTrace();
		}
	}
	
	public void initializeRPC(){
		try{XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
        configuration.setServerURL(new URL("http://"+variables.get("host")+
                                    ":"+variables.get("centralengineport")));
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
    public boolean uploadPluginsFile(){
        try{
            DOMSource source = new DOMSource(pluginsConfig);
            File file = new File(variables.get("pluginslocalgeneralconf"));
            Result result = new StreamResult(file);
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http:xml.apache.org/xslt}indent-amount","4");
            transformer.transform(source, result);
            c.cd(variables.get("remoteuserhome")+"/twister/config/");
            FileInputStream in = new FileInputStream(file);
            c.put(in, file.getName());
            in.close();
            System.out.println("Saved "+file.getName()+" to: "+
					variables.get("remoteuserhome")+"/twister/config/");
            return true;}
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
}
