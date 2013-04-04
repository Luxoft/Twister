/*
File: PanicDetect.java ; This file is part of Twister.
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

import java.awt.Color;
import java.awt.Component;
import java.io.File;
import java.io.FileInputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Properties;

import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextField;

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.twister.Item;
import com.twister.plugin.baseplugin.BasePlugin;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.w3c.dom.Document;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Result;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

public class PanicDetect extends BasePlugin implements TwisterPluginInterface {
	private static final long serialVersionUID = 1L;
	private JPanel p;
	private XmlRpcClient client;
	private ChannelSftp c;
	
	public static void main(String [] args){
		PanicDetect detect = new PanicDetect();
		detect.init(null, null, null, null);
		JFrame f = new JFrame();
		JPanel p = (JPanel)detect.getContent();
		p.setBackground(Color.blue);
		MyPanel p1 = detect.new MyPanel("regex",true,"185");
		p1.setLocation(10, 10);
		p.add(p1);
		f.add(p);
		f.setVisible(true);
		f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		f.setBounds(100,100,900,700);
	}

	@Override
	public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
			final Hashtable<String, String> variables,
			final Document pluginsConfig) {
		super.init(suite, suitetest, variables, pluginsConfig);
		System.out.println("Initializing " + getName() + " ...");
		//initializeSFTP();
		//initializeRPC();
		p = new JPanel();
		p.setLayout(null);
		//createXMLStructure();
		System.out.println(getName() + " initialized");
	}

	@Override
	public Component getContent() {
		return p;
	}

	@Override
	public String getDescription() {
		String description = "Panic detect plugin";
		return description;
	}

	@Override
	public String getFileName() {
		String filename = "PanicDetect.jar";
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
		String name = "PanicDetect";
		return name;
	}

	public void initializeSFTP() {
		try {
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
			c = (ChannelSftp) channel;
			System.out.println("SFTP successfully initialized");
		} catch (Exception e) {
			System.out.println("SFTP could not be initialized");
			e.printStackTrace();
		}
	}

	public void initializeRPC() {
		try {
			XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
			configuration.setServerURL(new URL("http://"
					+ variables.get("host") + ":"
					+ variables.get("centralengineport")));
			client = new XmlRpcClient();
			client.setConfig(configuration);
			System.out.println("Client initialized: " + client);
		} catch (Exception e) {
			System.out.println("Could not conect to " + variables.get("host")
					+ " :" + variables.get("centralengineport")
					+ "for RPC client initialization");
		}
	}

	/*
	 * method to copy plugins configuration file to server
	 */
	public boolean uploadPluginsFile() {
		try {
			DOMSource source = new DOMSource(pluginsConfig);
			File file = new File(variables.get("pluginslocalgeneralconf"));
			Result result = new StreamResult(file);
			TransformerFactory transformerFactory = TransformerFactory
					.newInstance();
			Transformer transformer = transformerFactory.newTransformer();
			transformer.setOutputProperty(OutputKeys.INDENT, "yes");
			transformer.setOutputProperty(
					"{http:xml.apache.org/xslt}indent-amount", "4");
			transformer.transform(source, result);
			c.cd(variables.get("remoteuserhome") + "/twister/config/");
			FileInputStream in = new FileInputStream(file);
			c.put(in, file.getName());
			in.close();
			System.out.println("Saved " + file.getName() + " to: "
					+ variables.get("remoteuserhome") + "/twister/config/");
			return true;
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}
	
	class MyPanel extends JPanel{
		private static final long serialVersionUID = 1L;
		private JTextField regex;
		private JCheckBox enabled;
		private JButton remove;
		private String id;
		
		public MyPanel(String regex, boolean enabled, String id) {
			this();
			this.regex.setText(regex);
			this.enabled.setSelected(enabled);
			this.id = id;
		}

		public MyPanel(){
			setLayout(null);
			setSize(400, 35);
			regex = new JTextField();
			enabled = new JCheckBox("Enabled");
			remove = new JButton("Remove");
			regex.setBounds(10, 5, 180, 25);
			add(regex);
			enabled.setBounds(210, 5, 80, 25);
			add(enabled);
			remove.setBounds(295, 5, 80, 25);
			add(remove);
		}

		public String getRegex() {
			return regex.getText();
		}

		public void setRegex(String regex) {
			this.regex.setText(regex);
		}

		public String getId() {
			return id;
		}

		public void setId(String id) {
			this.id = id;
		}
	}
}
