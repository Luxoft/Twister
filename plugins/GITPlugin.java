/*
File: GITPlugin.java ; This file is part of Twister.

Copyright (C) 2012 , Luxoft
Version: 3.004
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
import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.JTree;
import com.twister.CustomDialog;
import com.twister.Item;
import com.twister.MySftpBrowser;
import com.twister.plugin.baseplugin.BasePlugin;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreeSelectionModel;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import javax.swing.tree.DefaultTreeModel;

public class GITPlugin extends BasePlugin implements TwisterPluginInterface {
	private static final long serialVersionUID = 1L;
	private JCheckBox check;
    private JLabel parola,server,snapshot,username,branch;
    private JButton snap,update;
    private JTextField tparola,tserver,tsnapshot,tusername,tbranch;    
	private JPanel p;
	private DefaultMutableTreeNode root;
	private DefaultMutableTreeNode child2;
	private JTree tree;
	private JButton browse;
	private XmlRpcClient client;
	//private ChannelSftp c;
	private Node npassword,nserver,nsnapshot,ndefaultOp,nusername,nbranch;
	

	
	@Override
	public void init(ArrayList <Item>suite,ArrayList <Item>suitetest,
			  Hashtable<String, String>variables,
			  Document pluginsConfig,Applet container){
	
	//@Override
	//public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
	//		final Hashtable<String, String> variables,final Document pluginsConfig) {
		super.init(suite, suitetest, variables,pluginsConfig, container);
		System.out.println("Initializing "+getName()+" ...");
		//initializeSFTP();
		initializeRPC();
		p = new JPanel();
		
		username = new JLabel("Username: ");
		tusername = new JTextField();
        parola = new JLabel("Password: ");
        tparola = new JTextField();
        server = new JLabel("Server: ");
        tserver = new JTextField();
        branch = new JLabel("Branch: ");
        tbranch = new JTextField();
        snapshot = new JLabel("Snapshot: ");
        tsnapshot = new JTextField();
        snap = new JButton("Create snapshot");
        update = new JButton("Update");
        check = new JCheckBox("overwrite");
        browse = new JButton("...");
        
        //createXMLStructure();
        //uploadPluginsFile();
        
        npassword = getPropValue("password");
        nserver = getPropValue("server");
        nsnapshot = getPropValue("snapshot");
        ndefaultOp = getPropValue("default_operation");
        nusername = getPropValue("username");
        nbranch = getPropValue("branch");
        tparola.setText(npassword.getNodeValue());
        tserver.setText(nserver.getNodeValue());
        tsnapshot.setText(nsnapshot.getNodeValue());
        tusername.setText(nusername.getNodeValue());
        tbranch.setText(nbranch.getNodeValue());
        
        String operation = ndefaultOp.getNodeValue();
                
        if(!operation.equals("update")) check.setSelected(true);
        else check.setSelected(false);
        
        tparola.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
            	npassword.setNodeValue(tparola.getText());            	
            	uploadPluginsFile();
            }});
        tserver.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
            	nserver.setNodeValue(tserver.getText());
            	uploadPluginsFile();
            }});
        tsnapshot.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
            	nsnapshot.setNodeValue(tsnapshot.getText());
            	uploadPluginsFile();
            }});
        tusername.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
            	nusername.setNodeValue(tusername.getText());
            	uploadPluginsFile();
            }});
        tbranch.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
            	nbranch.setNodeValue(tbranch.getText());
            	uploadPluginsFile();
            }});
        check.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
            	if(!check.isSelected()){
            		ndefaultOp.setNodeValue("update");
            	}
            	else{
            		ndefaultOp.setNodeValue("overwrite");
            	}
            	uploadPluginsFile();
            }});
        
        snap.addActionListener(new ActionListener() {	
			public void actionPerformed(ActionEvent arg0) {
				final JFrame progress = createProgressBar();
				new Thread(){
					public void run(){
						snapshot(progress);
					}
				}.start();
			}
		});
        
        update.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {		
				final JFrame progress = createProgressBar();
				new Thread(){
					public void run(){
						update(progress);
					}
				}.start();
			}
		});        
        p.setLayout(null);
        username.setBounds(20, 30, 70, 25);
        parola.setBounds(20, 60, 70, 25);
        server.setBounds(20, 90, 70, 25);
        branch.setBounds(20, 120, 70, 25);
        snapshot.setBounds(20, 150, 70, 25);
        p.add(parola);
        p.add(server);
        p.add(branch);
        p.add(snapshot);
        p.add(username);        
        tsnapshot.setBounds(95, 150, 250, 25);
        tbranch.setBounds(95, 120, 250, 25);
        tserver.setBounds(95, 90, 250, 25);
        tparola.setBounds(95, 60, 250, 25);
        tusername.setBounds(95, 30, 250, 25);
        p.add(tparola);
        p.add(tbranch);
        p.add(tserver);
        p.add(tsnapshot);
        p.add(tusername);
        snap.setBounds(20,225, 130, 30);
        update.setBounds(155,225, 100, 30);
        check.setBounds(260,225, 100, 30);
        p.add(snap);
        p.add(update);
        p.add(check);
        browse.setBounds(350, 150, 50, 25);
        browse.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				selectSnapshot();
			}
		});
        p.add(browse);
        root = new DefaultMutableTreeNode("root", true);
        String dir = tsnapshot.getText();
        Object ob = null;
        try{ob = client.execute("file_size", new Object[]{dir});
            if(ob.toString().indexOf("*ERROR*")!=-1){
            	dir = variables.get("remoteuserhome")+"/twister/config/";
                //CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,p,"ERROR", ob.toString());
            }
        } catch (Exception e) {
            e.printStackTrace();
            if(ob!=null)System.out.println("Server response: "+ob.toString());
        }
        if(!dir.equals("")){
        	System.out.println("List files GIT plugin for: "+dir);
            try{ob = client.execute("list_files", new Object[]{dir,true});
                if(ob.toString().indexOf("*ERROR*")!=-1){
                    CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,p,"ERROR", ob.toString());
                }else{
                	try{HashMap hash = (HashMap)ob;
                		getList(root, hash,dir);
                	} catch (Exception e){
                		System.out.println("Could not build directory");
                		e.printStackTrace();
                	}
                }
            } catch (Exception e) {
                e.printStackTrace();
                if(ob!=null)System.out.println("Server response: "+ob.toString());
            }
        }
        
        
        tree = new JTree(root);
		tree.expandRow(1);
		tree.setDragEnabled(true);
		tree.setRootVisible(false);
		tree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
		
		JScrollPane scroll = new JScrollPane(tree);
		scroll.setBounds(10, 20, 480, 470);
		JPanel panel = new JPanel();
		panel.setBorder(BorderFactory.createTitledBorder("Snapshot location preview"));
		panel.setLayout(null);
		panel.setBounds(410, 10, 500, 500);
		panel.add(scroll);
		p.add(panel);
		System.out.println(getName()+" initialized");
	}


	@Override
	public Component getContent() {
		return p;
	}

	@Override
	public String getFileName() {
		String filename = "GITPlugin.jar";
		return filename;
	}

	@Override
	public void terminate() {
		super.terminate();
		check= null;
		username = null;
	    parola = null;
	    server = null;
	    snapshot = null;
	    snap = null;
	    update = null;
	    tparola = null;
	    tserver = null;
	    tsnapshot = null;
	    tusername = null;
		root = null;
		child2 = null;
		tree = null;
		p = null;
	}

	@Override
	public String getName() {
		String name = "GITPlugin";
		return name;
	}
	
	/*
	 * method to create a progress bar
	 * window
	 */
	public JFrame createProgressBar(){
		JFrame progress = new JFrame();
		progress.setAlwaysOnTop(true);
		progress.setLocation(400,600);
		progress.setUndecorated(true);
		JProgressBar bar = new JProgressBar();
		bar.setIndeterminate(true);
		progress.add(bar);
		progress.pack();
		progress.setVisible(true);
		return progress;
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
	
	public void selectSnapshot(){
        try{
        	final String initial = tsnapshot.getText();
        	final MySftpBrowser browser = new MySftpBrowser(variables.get("host"),
        													variables.get("user"), 
        													variables.get("password"), 
        													variables.get("centralengineport"),
        													tsnapshot, p,false);
        	//final MySftpBrowser browser = new MySftpBrowser(c, tsnapshot, p);
        	new Thread(){
        		public void run(){
        			while(browser.isVisible()){
                		try {
							Thread.sleep(100);
						} catch (InterruptedException e) {
							e.printStackTrace();
						}
                	}
        			if (!initial.equals(tsnapshot.getText())){        				
        				nsnapshot.setNodeValue(tsnapshot.getText());  
        				uploadPluginsFile();
        				JFrame progress = new JFrame();
        				progress.setAlwaysOnTop(true);
        				progress.setLocation(400,600);
        				progress.setUndecorated(true);
        				JProgressBar bar = new JProgressBar();
        				bar.setIndeterminate(true);
        				progress.add(bar);
        				progress.pack();
        				refreshTree(tsnapshot.getText(),progress);}
        		}
        	}.start();
        }
        catch(Exception e){
            e.printStackTrace();}
	}
	
	/*
	 * refresh tree structure
	 */
	public void refreshTree(final String home,final JFrame frame) {
		new Thread() {
			public void run() {
				frame.setVisible(true);
				refreshStructure(home);
				frame.dispose();
			}
		}.start();
	}
	
	/*
	 * get folder structure from CE
	 */
	public void refreshStructure(String home) {
		try {
			root.remove(0);
			if(!home.equals("")){
				Object ob = null;
	            System.out.println("List files GIT");
		        try{ob = client.execute("list_files", new Object[]{home,true});
		            if(ob.toString().indexOf("*ERROR*")!=-1){
		                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,p,"ERROR", ob.toString());
		            }else{
		            	HashMap hash = (HashMap)ob;
			            getList(root, hash,home);
			            ((DefaultTreeModel) tree.getModel()).reload();
			    		tree.expandRow(0);
		            }
		        } catch (Exception e) {
		            System.out.println("Server response: "+ob.toString());
		            e.printStackTrace();
		        }
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		
	}
		
	
	/*
     * construct the list for folders representation in jtree
     */
    public void getList(DefaultMutableTreeNode node, HashMap hash, String curentdir) {
        try {
            DefaultMutableTreeNode child = new DefaultMutableTreeNode(curentdir);
            node.add(child);
            Object [] children = (Object [])hash.get("children");
            if(children!=null&&children.length>0){
                for(Object subchild:children){
                    String name = ((HashMap)subchild).get("data").toString();
                    if(((HashMap)subchild).get("folder")!=null){//folder
                        getList(child, (HashMap)subchild ,curentdir+"/"+name);
                    } else {//file
                        child2 = new DefaultMutableTreeNode(name);
                        child.add(child2);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
	
	/*
	 * snapshot method triggered by
	 * user on button press
	 */
	public void snapshot(JFrame frame){
		try {
			boolean exists = true;
			String folder = tsnapshot.getText();
			
			Object ob = null;
			try{ob = client.execute("file_size", new Object[]{folder});
            	if(ob.toString().indexOf("*ERROR*")!=-1){
            		exists = false;
            	}
			} catch (Exception e) {
				exists = false;
				System.out.println("Server response: "+ob.toString());
				e.printStackTrace();
			}
			if(exists){
				int response = JOptionPane.showConfirmDialog(this, "Warning, "+folder+
															 " allready exist, continue?","Warning",
															 JOptionPane.OK_CANCEL_OPTION);
				if(response==JOptionPane.CANCEL_OPTION){
					frame.dispose();
					return;
				}
			}
			String param="command=snapshot";
			String result = client.execute("run_plugin", new Object[]{variables.get("user"),
																	 getName(),param})+"";
			if(result.equals("true")){
				frame.setVisible(false);
				JOptionPane.showConfirmDialog(GITPlugin.this, "Success",
											  "Snapshot", JOptionPane.CLOSED_OPTION, 
											  JOptionPane.INFORMATION_MESSAGE);
				refreshTree(tsnapshot.getText(),frame); 
			}
			else{
				frame.dispose();
				JOptionPane.showConfirmDialog(GITPlugin.this, "Snapshot operation"+
													" failed with error:\n "+result, 
													"Snapshot", JOptionPane.CLOSED_OPTION,
													JOptionPane.WARNING_MESSAGE);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/*
	 * update method triggered by
	 * user on button press
	 */
	public void update(JFrame frame){
		try {String param;
			if(!check.isSelected()){
				param = "command=update&overwrite=false";}
			else{
				param = "command=update&overwrite=true";}
			String result = client.execute("run_plugin", new Object[]{variables.get("user"),
																	 getName(),param})+"";
			if(result.equals("true")){
				frame.setVisible(false);
				JOptionPane.showConfirmDialog(GITPlugin.this, "Success",
						  					  "Snapshot", JOptionPane.CLOSED_OPTION, 
						  					  JOptionPane.INFORMATION_MESSAGE);
				refreshTree(tsnapshot.getText(),frame);}
			else{
				frame.dispose();
				JOptionPane.showConfirmDialog(GITPlugin.this, "Update operation"+
													" failed with error:\n "+result, 
						  					   "Snapshot", JOptionPane.CLOSED_OPTION,
						  					  		   JOptionPane.WARNING_MESSAGE);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}

