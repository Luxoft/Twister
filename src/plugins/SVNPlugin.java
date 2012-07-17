import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.io.File;
import java.io.FileInputStream;
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
import org.w3c.dom.Node;
import javax.swing.tree.DefaultTreeModel;
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
    private JLabel parola,server,snapshot,username;
    private JButton snap,update;
    private JTextField tparola,tserver,tsnapshot,tusername;    
	private JPanel p;
	private DefaultMutableTreeNode root;
	private DefaultMutableTreeNode child2;
	private JTree tree;
	private JButton browse;
	private XmlRpcClient client;
	private ChannelSftp c;
	private VFSJFileChooser filechooser;
	private Node npassword,nserver,nsnapshot,ndefaultOp,nusername;
	

	@Override
	public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
			final Hashtable<String, String> variables,final Document pluginsConfig) {
		super.init(suite, suitetest, variables,pluginsConfig);
		System.out.println("Initializing "+getName()+" ...");
		initializeSFTP();
		initializeRPC();
		p = new JPanel();
		
		username = new JLabel("Username: ");
		tusername = new JTextField();
        parola = new JLabel("Password: ");
        tparola = new JTextField();
        server = new JLabel("Server: ");
        tserver = new JTextField();
        snapshot = new JLabel("Snapshot: ");
        tsnapshot = new JTextField();
        snap = new JButton("Create snaphot");
        update = new JButton("Update");
        check = new JCheckBox("overwrite");
        browse = new JButton("...");
        
        createXMLStructure();
        
        npassword = getPropValue("password");
        nserver = getPropValue("server");
        nsnapshot = getPropValue("snapshot");
        ndefaultOp = getPropValue("default_operation");
        nusername = getPropValue("username");
        
        //if(!npassword.getNodeValue().equals(" ")){
        	tparola.setText(npassword.getNodeValue());
        //	}
        //if(!nserver.getNodeValue().equals(" ")){
        	tserver.setText(nserver.getNodeValue());
        //	}
        //if(!nsnapshot.getNodeValue().equals(" ")){
        	tsnapshot.setText(nsnapshot.getNodeValue());
        //	}
        //if(!nusername.getNodeValue().equals(" ")){
        	tusername.setText(nusername.getNodeValue());
        //	}
        
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
        snapshot.setBounds(20, 120, 70, 25);
        p.add(parola);
        p.add(server);
        p.add(snapshot);
        p.add(username);
        
        tsnapshot.setBounds(95, 120, 250, 25);
        tserver.setBounds(95, 90, 250, 25);
        tparola.setBounds(95, 60, 250, 25);
        tusername.setBounds(95, 30, 250, 25);
        p.add(tparola);
        p.add(tserver);
        p.add(tsnapshot);
        p.add(tusername);
        
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
        	try{c.cd(tsnapshot.getText());}
        	catch(Exception e){e.printStackTrace();
        		try {
					c.cd(variables.get("remoteuserhome")+
							"/twister/config/");
				} catch (SftpException e1) {
					e1.printStackTrace();
				}
        	}
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
                safeName = safeName.substring(safeName.indexOf(variables.get("host"))+
                		variables.get("host").length());
                String [] check = safeName.split("/");
                if(check[check.length-1].equals(check[check.length-2])){
                    StringBuffer buffer = new StringBuffer();
                    for(int i=0;i<check.length-1;i++){
                        buffer.append(check[i]+"/");}
                    safeName = buffer.toString();}
                tsnapshot.setText(safeName);
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
				refreshStructure(home);
				frame.dispose();
			}
		}.start();
	}
	
	public void refreshStructure(String home) {
		try {c.cd(home);
			root.remove(0);
			getList(root,c,true);
		} catch (Exception e) {
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
	
	/*
	 * snapshot method triggered by
	 * user on button press
	 */
	public void snapshot(JFrame frame){
		try {
			String param="command=snapshot";
			String result = client.execute("runPlugin", new Object[]{variables.get("user"),
																	 getName(),param})+"";
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
			String result = client.execute("runPlugin", new Object[]{variables.get("user"),
																	 getName(),param})+"";
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