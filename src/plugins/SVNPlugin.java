import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;
import java.io.File;
import java.io.FileInputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Hashtable;
import java.util.Properties;
import java.util.Vector;

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

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.SftpException;
import com.twister.Item;
import com.twister.plugin.baseplugin.BasePlugin;
import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreeSelectionModel;

import net.sf.vfsjfilechooser.VFSJFileChooser;
import net.sf.vfsjfilechooser.VFSJFileChooser.RETURN_TYPE;
import net.sf.vfsjfilechooser.utils.VFSUtils;

import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Element;
import javax.swing.tree.DefaultTreeModel;
import javax.xml.stream.XMLResolver;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Result;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.apache.commons.vfs.FileObject;

public class SVNPlugin extends BasePlugin implements TwisterPluginInterface {
	private static final long serialVersionUID = 1L;
	private JCheckBox check;
    private JLabel parola,server,snapshot;
    private JButton snap,update;
    private JTextField tparola,tserver,tsnapshot;    
	private JPanel p;
	private DefaultMutableTreeNode root;
	private DefaultMutableTreeNode child2;
	private JTree tree;
	private JButton browse;
	private XmlRpcClient client;
	private ChannelSftp c;
	private VFSJFileChooser filechooser;
	

	@Override
	public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
			final Hashtable<String, String> variables,Document pluginsConfig) {
		super.init(suite, suitetest, variables,pluginsConfig);
		System.out.println("Initializing "+getName()+" ...");
		initializeSFTP();
		initializeRPC();
		p = new JPanel();
		
        parola = new JLabel("Password: ");
        tparola = new JTextField();
        server = new JLabel("Server: ");
        tserver = new JTextField();
        snapshot = new JLabel("Snapshot: ");
        tsnapshot = new JTextField();
        snap = new JButton("Create snaphot");
        update = new JButton("Update");
        check = new JCheckBox("update");
        browse = new JButton("...");
        
        createXMLStructure();

        tparola.setText(getPasswordFromConfig());
        tserver.setText(getServerFromConfig());
        tsnapshot.setText(getSnapshotFromConfig());
        String operation = getDefaultOperationFromConfig();
        if(operation.equals("update")) check.setSelected(true);
        else check.setSelected(false);
        
        tparola.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
            	savePasswordToConfig(tparola.getText());
            }});
        tserver.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
            	saveServerToConfig(tserver.getText());
            }});
        tsnapshot.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
            	saveSnapshotToConfig(tsnapshot.getText());
            }});
        check.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
            	if(check.isSelected()){
            		saveDefaultOperationToConfig("update");
            	}
            	if(!check.isSelected()){
            		saveDefaultOperationToConfig("overwrite");
            	}
            }});
        
        snap.addActionListener(new ActionListener() {	
			public void actionPerformed(ActionEvent arg0) {
				final JFrame progress = new JFrame();
				progress.setLocation(400,600);
				progress.setUndecorated(true);
				JProgressBar bar = new JProgressBar();
				bar.setIndeterminate(true);
				progress.add(bar);
				progress.pack();
				progress.setVisible(true);
				new Thread(){
					public void run(){
						snapshot(progress);
					}
				}.start();
			}
		});
        
        update.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {		
				final JFrame progress = new JFrame();
				progress.setAlwaysOnTop(true);
				progress.setLocation(400,600);
				progress.setUndecorated(true);
				JProgressBar bar = new JProgressBar();
				bar.setIndeterminate(true);
				progress.add(bar);
				progress.pack();
				progress.setVisible(true);
				new Thread(){
					public void run(){
						update(progress);
					}
				}.start();
			}
		});
        
        p.setLayout(null);
        parola.setBounds(20, 60, 70, 25);
        server.setBounds(20, 90, 70, 25);
        snapshot.setBounds(20, 120, 70, 25);
        p.add(parola);
        p.add(server);
        p.add(snapshot);
        tsnapshot.setBounds(95, 120, 250, 25);
        tserver.setBounds(95, 90, 250, 25);
        tparola.setBounds(95, 60, 250, 25);
        p.add(tparola);
        p.add(tserver);
        p.add(tsnapshot);
        
        snap.setBounds(20,195, 130, 30);
        update.setBounds(155,195, 100, 30);
        check.setBounds(260,195, 100, 30);
        p.add(snap);
        p.add(update);
        p.add(check);
        
        browse.setBounds(350, 120, 50, 25);
        browse.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent arg0) {
				selectSnapshot();
			}
		});
        p.add(browse);        
        
        root = new DefaultMutableTreeNode("root", true);
        if(c!=null){
        	System.out.println("getting list from ");
        	try{System.out.print(tsnapshot.getText());
        		c.cd(tsnapshot.getText());}
        	catch(Exception e){e.printStackTrace();}
        	getList(root, c, true);
        }
        else{
        	System.out.println("SFTP connection not initialized");
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
	public String getDescription() {
		String description = "SVNPlugin";
		return description;
	}

	@Override
	public String getFileName() {
		String filename = "SVNPlugin.jar";
		return filename;
	}

	@Override
	public void terminate() {
		super.terminate();
		check= null;
	    parola = null;
	    server = null;
	    snapshot = null;
	    snap = null;
	    update = null;
	    tparola = null;
	    tserver = null;
	    tsnapshot = null;
		root = null;
		c = null;
		child2 = null;
		tree = null;
		p = null;
	}

	@Override
	public String getName() {
		String name = "SVNPlugin";
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
	
	public void initalizeChooser(){
		filechooser = new VFSJFileChooser("sftp://"+variables.get("user")+":"+
                variables.get("password")+"@"+variables.get("host")+
                "/home/"+variables.get("user")+"/twister/config/");        
		filechooser.setFileHidingEnabled(true);
		filechooser.setMultiSelectionEnabled(false);
		filechooser.setFileSelectionMode(VFSJFileChooser.SELECTION_MODE.FILES_AND_DIRECTORIES);
	}
	
	public void selectSnapshot(){
        try{if(filechooser==null)initalizeChooser();
        	RETURN_TYPE answer = filechooser.showOpenDialog(SVNPlugin.this);
            if (answer == RETURN_TYPE.APPROVE){
                FileObject aFileObject = filechooser.getSelectedFile();
                
                String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
                System.out.println(safeName);
                safeName = safeName.substring(safeName.indexOf(variables.get("host"))+
                		variables.get("host").length());
                String [] check = safeName.split("/");
                if(check[check.length-1].equals(check[check.length-2])){
                    StringBuffer buffer = new StringBuffer();
                    for(int i=0;i<check.length-1;i++){
                        buffer.append(check[i]+"/");}
                    safeName = buffer.toString();}
                tsnapshot.setText(safeName);
                saveSnapshotToConfig(tsnapshot.getText());    
                JFrame progress = new JFrame();
				progress.setAlwaysOnTop(true);
				progress.setLocation(400,600);
				progress.setUndecorated(true);
				JProgressBar bar = new JProgressBar();
				bar.setIndeterminate(true);
				progress.add(bar);
				progress.pack();
                refreshTree(safeName,progress);}
            }
         catch(Exception e){
             filechooser=null;
             e.printStackTrace();}
	}
	
	/*
	 * refresh tree structure
	 */
	public void refreshTree(final String home,final JFrame frame) {
		new Thread() {
			public void run() {
				frame.setVisible(true);
				System.out.println("home:"+home);
				refreshStructure(home);
				frame.dispose();
			}
		}.start();
	}
	
	public void refreshStructure(String home) {
		try {
			if(c==null)System.out.println("c is null");
			System.out.println("home:"+home);
			c.cd(home);
			root.remove(0);
			getList(root,c,true);
		} catch (Exception e) {
			System.out.println("HOME: "+home);
			e.printStackTrace();
		}
		((DefaultTreeModel) tree.getModel()).reload();
		tree.expandRow(0);
	}
	
	/*
	 * construct the list for folders representation in jtree
	 */
	public void getList(DefaultMutableTreeNode node,
						ChannelSftp c, boolean addfirst) {
		try {
			DefaultMutableTreeNode child = new DefaultMutableTreeNode(c.pwd());
			Vector<LsEntry> vector1 = c.ls(".");
			Vector<String> vector = new Vector<String>();
			Vector<String> folders = new Vector<String>();
			Vector<String> files = new Vector<String>();
			int lssize = vector1.size();
			if(addfirst){
				node.add(child);
				addfirst=false;
			}
			else{
				if (lssize > 2) {
					node.add(child);
				}
			}			
			String current;
			for (int i = 0; i < lssize; i++) {
				if (vector1.get(i).getFilename().split("\\.").length == 0) {
					continue;
				}
				try {
				    current = c.pwd();
					c.cd(vector1.get(i).getFilename());
					c.cd(current);
					folders.add(vector1.get(i).getFilename());
				} catch (SftpException e) {
					if (e.id == 4) {
						files.add(vector1.get(i).getFilename());
					}
					else{
					       e.printStackTrace();
					   }
				}
			}
			Collections.sort(folders);
			Collections.sort(files);
			for (int i = 0; i < folders.size(); i++) {
				vector.add(folders.get(i));
			}
			for (int i = 0; i < files.size(); i++) {
				vector.add(files.get(i));
			}
			for (int i = 0; i < vector.size(); i++) {
				try {
				    current = c.pwd();
					c.cd(vector.get(i));
					getList(child, c,false);
					c.cd(current);
				} catch (SftpException e) {
					if (e.id == 4) {
						child2 = new DefaultMutableTreeNode(vector.get(i));
						child.add(child2);
					} else {
						e.printStackTrace();
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public void treeClickReleased(MouseEvent ev){
		if ((tree.getSelectionPath()!=null) &&
		(!tree.getModel().isLeaf(tree.getSelectionPath()
		.getLastPathComponent()))) {
			String thefile = tree.getSelectionPath().getLastPathComponent().
																 toString();
			tsnapshot.setText(thefile);
		}}
	
	public void snapshot(JFrame frame){
		try {
			String param="command=snapshot";
			String result = client.execute("runPlugin", new Object[]{variables.get("user"),
																	 getName(),param})+"";
			System.out.println(result);
			if(result.equals("true")){
				frame.setVisible(false);
				JOptionPane.showConfirmDialog(SVNPlugin.this, "Success",
											  "Snaphot", JOptionPane.CLOSED_OPTION, 
											  JOptionPane.INFORMATION_MESSAGE);
				refreshTree(tsnapshot.getText(),frame); 
			}
			else{
				frame.dispose();
				JOptionPane.showConfirmDialog(SVNPlugin.this, "Snapshot operation"+
													" failed with error:\n "+result, 
													"Snaphot", JOptionPane.CLOSED_OPTION,
													JOptionPane.WARNING_MESSAGE);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	
	public void update(JFrame frame){
		try {String param;
			if(check.isSelected()){
				param = "command=update&overwrite=false";}
			else{
				param = "command=update&overwrite=true";}
			String result = client.execute("runPlugin", new Object[]{variables.get("user"),
																	 getName(),param})+"";
			System.out.println(result);
			if(result.equals("true")){
				frame.setVisible(false);
				JOptionPane.showConfirmDialog(SVNPlugin.this, "Success",
						  					  "Snaphot", JOptionPane.CLOSED_OPTION, 
						  					  JOptionPane.INFORMATION_MESSAGE);
				refreshTree(tsnapshot.getText(),frame);}
			else{
				frame.dispose();
				JOptionPane.showConfirmDialog(SVNPlugin.this, "Update operation"+
													" failed with error:\n "+result, 
						  					   "Snaphot", JOptionPane.CLOSED_OPTION,
						  					  		   JOptionPane.WARNING_MESSAGE);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/*
	 * method to check and create XML structure
	 * for this plugin
	 */
	public void createXMLStructure(){
		Document doc = pluginsConfig;
        NodeList list1 = doc.getElementsByTagName("Plugin");
        Element item;
        Element compare;
        boolean found = false;
        for(int i=0;i<list1.getLength();i++){
            item = (Element)list1.item(i);
            compare = (Element)item.getElementsByTagName("jarfile").item(0);
            if(compare.getChildNodes().item(0).getNodeValue().equals(getFileName())){
            	found = true;
            }
        }
        if(!found){
        	
        	Element rootElement = doc.createElement("Plugin");
        	doc.getFirstChild().appendChild(rootElement);
            Element em2 = doc.createElement("name");
            em2.appendChild(doc.createTextNode(getName()));
            rootElement.appendChild(em2);
            em2 = doc.createElement("jarfile");
            em2.appendChild(doc.createTextNode(getFileName()));
            rootElement.appendChild(em2);
            em2 = doc.createElement("pyfile");
            String filename = getFileName().split(".jar")[0]+".py";
            em2.appendChild(doc.createTextNode(filename));
            rootElement.appendChild(em2);
            em2 = doc.createElement("status");
            em2.appendChild(doc.createTextNode("disabled"));
            rootElement.appendChild(em2);
            
            em2 = doc.createElement("property");
            
            Element em3 = doc.createElement("propname");            
            em3.appendChild(doc.createTextNode("default_operation"));            
            em2.appendChild(em3);
            
            Element em4 = doc.createElement("propvalue");            
            em4.appendChild(doc.createTextNode("disabled"));            
            em2.appendChild(em4);
            
            rootElement.appendChild(em2);
            
            em2 = doc.createElement("property");
            
            em3 = doc.createElement("propname");            
            em3.appendChild(doc.createTextNode("snapshot"));            
            em2.appendChild(em3);
            
            em4 = doc.createElement("propvalue");            
            em4.appendChild(doc.createTextNode(""));            
            em2.appendChild(em4);
            
            rootElement.appendChild(em2);
            
            
            em2 = doc.createElement("property");
            
            em3 = doc.createElement("propname");            
            em3.appendChild(doc.createTextNode("server"));            
            em2.appendChild(em3);
            
            em4 = doc.createElement("propvalue");            
            em4.appendChild(doc.createTextNode(""));            
            em2.appendChild(em4);
            
            rootElement.appendChild(em2);            
            
            em2 = doc.createElement("property");
            
            em3 = doc.createElement("propname");            
            em3.appendChild(doc.createTextNode("password"));            
            em2.appendChild(em3);
            
            em4 = doc.createElement("propvalue");            
            em4.appendChild(doc.createTextNode(""));            
            em2.appendChild(em4);
            
            rootElement.appendChild(em2);
        	
        }
	}
	
	/*
	 * method to save default operation 
	 * to doc provided by Twister
	 */
	public void saveDefaultOperationToConfig(String operation){	
		Document doc = pluginsConfig;
        NodeList list1 = doc.getElementsByTagName("Plugin");
        Element item;
        Element compare;
        for(int i=0;i<list1.getLength();i++){
            item = (Element)list1.item(i);
            compare = (Element)item.getElementsByTagName("jarfile").item(0);
            if(compare.getChildNodes().item(0).getNodeValue().equals(getFileName())){
            	NodeList list2 = item.getElementsByTagName("property");
            	for(int j=0;j<list2.getLength();j++){
                    item = (Element)list2.item(j);
                    compare = (Element)item.getElementsByTagName("propname").item(0);
                    if(compare.getChildNodes().item(0).getNodeValue().equals("default_operation")){
                    	compare = (Element)item.getElementsByTagName("propvalue").item(0);
                    	try{compare.getChildNodes().item(0).setNodeValue(operation);}
                    	catch(Exception e){
                    		compare.appendChild(doc.createTextNode(operation));}
                    	uploadPluginsFile();
                    }
            	}
            }
        }
	}
	
	/*
	 * method to save snapshot to
	 *  doc provided by Twister
	 */
	public void saveSnapshotToConfig(String snapshot){	
		Document doc = pluginsConfig;
        NodeList list1 = doc.getElementsByTagName("Plugin");
        Element item;
        Element compare;
        for(int i=0;i<list1.getLength();i++){
            item = (Element)list1.item(i);
            compare = (Element)item.getElementsByTagName("jarfile").item(0);
            if(compare.getChildNodes().item(0).getNodeValue().equals(getFileName())){
            	NodeList list2 = item.getElementsByTagName("property");
            	for(int j=0;j<list2.getLength();j++){
                    item = (Element)list2.item(j);
                    compare = (Element)item.getElementsByTagName("propname").item(0);
                    if(compare.getChildNodes().item(0).getNodeValue().equals("snapshot")){
                    	compare = (Element)item.getElementsByTagName("propvalue").item(0);
                    	try{compare.getChildNodes().item(0).setNodeValue(snapshot);}
                    	catch(Exception e){
                    		compare.appendChild(doc.createTextNode(snapshot));}
                    	uploadPluginsFile();
                    }
            	}
            }
        }
	}
	
	/*
	 * method to save server to
	 * doc provided by Twister
	 */
	public void saveServerToConfig(String server){	
		Document doc = pluginsConfig;
        NodeList list1 = doc.getElementsByTagName("Plugin");
        Element item;
        Element compare;
        for(int i=0;i<list1.getLength();i++){
            item = (Element)list1.item(i);
            compare = (Element)item.getElementsByTagName("jarfile").item(0);
            if(compare.getChildNodes().item(0).getNodeValue().equals(getFileName())){
            	NodeList list2 = item.getElementsByTagName("property");
            	for(int j=0;j<list2.getLength();j++){
                    item = (Element)list2.item(j);
                    compare = (Element)item.getElementsByTagName("propname").item(0);
                    if(compare.getChildNodes().item(0).getNodeValue().equals("server")){
                    	compare = (Element)item.getElementsByTagName("propvalue").item(0);
                    	try{compare.getChildNodes().item(0).setNodeValue(server);}
                    	catch(Exception e){
                    		compare.appendChild(doc.createTextNode(server));}
                    	uploadPluginsFile();
                    }
            	}
            }
        }
	}

	/*
	 * method to save password 
	 * to doc provided by Twister
	 */
	public void savePasswordToConfig(String password){	
		Document doc = pluginsConfig;
        NodeList list1 = doc.getElementsByTagName("Plugin");
        Element item;
        Element compare;
        for(int i=0;i<list1.getLength();i++){
            item = (Element)list1.item(i);
            compare = (Element)item.getElementsByTagName("jarfile").item(0);
            if(compare.getChildNodes().item(0).getNodeValue().equals(getFileName())){
            	NodeList list2 = item.getElementsByTagName("property");
            	for(int j=0;j<list2.getLength();j++){
                    item = (Element)list2.item(j);
                    compare = (Element)item.getElementsByTagName("propname").item(0);
                    if(compare.getChildNodes().item(0).getNodeValue().equals("password")){
                    	compare = (Element)item.getElementsByTagName("propvalue").item(0);
                    	try{compare.getChildNodes().item(0).setNodeValue(password);}
                    	catch(Exception e){
                    		compare.appendChild(doc.createTextNode(password));}
                    	uploadPluginsFile();
                    }
            	}
            }
        }
	}
	
	/*
	 * method to retrieve default operation saved
	 * in doc provided by Twister
	 */
	public String getDefaultOperationFromConfig(){	
		Document doc = pluginsConfig;
        NodeList list1 = doc.getElementsByTagName("Plugin");
        Element item;
        Element compare;
        for(int i=0;i<list1.getLength();i++){
            item = (Element)list1.item(i);
            compare = (Element)item.getElementsByTagName("jarfile").item(0);
            if(compare.getChildNodes().item(0).getNodeValue().equals(getFileName())){
            	NodeList list2 = item.getElementsByTagName("property");
            	for(int j=0;j<list2.getLength();j++){
                    item = (Element)list2.item(j);
                    compare = (Element)item.getElementsByTagName("propname").item(0);
                    if(compare.getChildNodes().item(0).getNodeValue().equals("default_operation")){
                    	compare = (Element)item.getElementsByTagName("propvalue").item(0);
                    	try{return compare.getChildNodes().item(0).getNodeValue();}
                    	catch(Exception e){return "";}
                    }
            	}
            	
            	item = (Element)list1.item(i);
            	Element em2 = doc.createElement("property");
                
                Element em3 = doc.createElement("propname");            
                em3.appendChild(doc.createTextNode("default_operation"));            
                em2.appendChild(em3);
                
                Element em4 = doc.createElement("propvalue");            
                em4.appendChild(doc.createTextNode("disabled"));            
                em2.appendChild(em4);
                
                item.appendChild(em2);            	
         
                return "disabled";
            }
        }
        return "";
	}
	
	/*
	 * method to retrieve snapshot location saved
	 * in doc provided by Twister
	 */
	public String getSnapshotFromConfig(){	
		Document doc = pluginsConfig;
        NodeList list1 = doc.getElementsByTagName("Plugin");
        Element item;
        Element compare;
        for(int i=0;i<list1.getLength();i++){
            item = (Element)list1.item(i);
            compare = (Element)item.getElementsByTagName("jarfile").item(0);
            if(compare.getChildNodes().item(0).getNodeValue().equals(getFileName())){
            	NodeList list2 = item.getElementsByTagName("property");
            	for(int j=0;j<list2.getLength();j++){
                    item = (Element)list2.item(j);
                    compare = (Element)item.getElementsByTagName("propname").item(0);
                    if(compare.getChildNodes().item(0).getNodeValue().equals("snapshot")){
                    	compare = (Element)item.getElementsByTagName("propvalue").item(0);
                    	try{return compare.getChildNodes().item(0).getNodeValue();}
                    	catch(Exception e){return "";}
                    }
            	}
            	
            	item = (Element)list1.item(i);
            	Element em2 = doc.createElement("property");
                
                Element em3 = doc.createElement("propname");            
                em3.appendChild(doc.createTextNode("snapshot"));            
                em2.appendChild(em3);
                
                Element em4 = doc.createElement("propvalue");            
                em4.appendChild(doc.createTextNode(""));            
                em2.appendChild(em4);
                
                item.appendChild(em2);            	
         
                return "";
            }
        }
        return null;
	}
	
	/*
	 * method to retrieve server saved
	 * in doc provided by Twister
	 */
	public String getServerFromConfig(){	
		Document doc = pluginsConfig;
        NodeList list1 = doc.getElementsByTagName("Plugin");
        Element item;
        Element compare;
        for(int i=0;i<list1.getLength();i++){
            item = (Element)list1.item(i);
            compare = (Element)item.getElementsByTagName("jarfile").item(0);
            if(compare.getChildNodes().item(0).getNodeValue().equals(getFileName())){
            	NodeList list2 = item.getElementsByTagName("property");
            	for(int j=0;j<list2.getLength();j++){
                    item = (Element)list2.item(j);
                    compare = (Element)item.getElementsByTagName("propname").item(0);
                    if(compare.getChildNodes().item(0).getNodeValue().equals("server")){
                    	compare = (Element)item.getElementsByTagName("propvalue").item(0);
                    	try{return compare.getChildNodes().item(0).getNodeValue();}
                    	catch(Exception e){return "";}
                    }
            	}
            	
            	item = (Element)list1.item(i);
            	Element em2 = doc.createElement("property");
                
                Element em3 = doc.createElement("propname");            
                em3.appendChild(doc.createTextNode("server"));            
                em2.appendChild(em3);
                
                Element em4 = doc.createElement("propvalue");            
                em4.appendChild(doc.createTextNode(""));            
                em2.appendChild(em4);
                
                item.appendChild(em2);            	
         
                return "";
            }
        }
        return null;
	}

	/*
	 * method to retrieve password saved
	 * in doc provided by Twister
	 */
	public String getPasswordFromConfig(){	
		Document doc = pluginsConfig;
        NodeList list1 = doc.getElementsByTagName("Plugin");
        Element item;
        Element compare;
        for(int i=0;i<list1.getLength();i++){
            item = (Element)list1.item(i);
            compare = (Element)item.getElementsByTagName("jarfile").item(0);
            if(compare.getChildNodes().item(0).getNodeValue().equals(getFileName())){
            	NodeList list2 = item.getElementsByTagName("property");
            	for(int j=0;j<list2.getLength();j++){
                    item = (Element)list2.item(j);
                    compare = (Element)item.getElementsByTagName("propname").item(0);
                    if(compare.getChildNodes().item(0).getNodeValue().equals("password")){
                    	compare = (Element)item.getElementsByTagName("propvalue").item(0);
                    	try{return compare.getChildNodes().item(0).getNodeValue();}
                    	catch(Exception e){return "";}
                    }
            	}
            	
            	item = (Element)list1.item(i);
            	Element em2 = doc.createElement("property");
                
                Element em3 = doc.createElement("propname");            
                em3.appendChild(doc.createTextNode("password"));            
                em2.appendChild(em3);
                
                Element em4 = doc.createElement("propvalue");            
                em4.appendChild(doc.createTextNode(""));            
                em2.appendChild(em4);
                
                item.appendChild(em2);            	
         
                return "";
            }
        }
        return null;
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
            transformer.setOutputProperty("{http:xml.apache.org/xslt}indent-amount",
            																	 "4");
            transformer.transform(source, result);
            System.out.println("cd to: "+variables.get("remoteuserhome")+
            											"/twister/config/");
            if(c==null)System.out.println("C is null");
            c.cd(variables.get("remoteuserhome")+"/twister/config/");
            System.out.println("Saving "+file.getName()+" to: "+
            					variables.get("remoteuserhome")+"/twister/config/");
            FileInputStream in = new FileInputStream(file);
            c.put(in, file.getName());
            in.close();
            return true;}
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
}