import javax.swing.JTree;
import javax.swing.JScrollPane;
import javax.swing.tree.DefaultMutableTreeNode;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathFactory;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathConstants;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.tree.TreePath;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import com.twister.CustomDialog;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.Result;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.OutputKeys;
import javax.swing.JTextField;
import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.BoxLayout;
import java.awt.BorderLayout;
import java.io.FileInputStream;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.Channel;
import java.util.Properties;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class Globals {
    private ChannelSftp ch ;
    public JScrollPane panel;
    private JTree tree;
    private XPath xpath;
    private Document doc;
    private DefaultMutableTreeNode root;
    private File globalsfile;
    private boolean finished = true;
    
    public Globals(){
        initSftp();
        parseDocument();
        init();
        buildTree();
    }
    
    public void refresh(){
        parseDocument();
        buildTree();
    }
    
    public void parseDocument(){
        try{DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            globalsfile = getGlobalsFile();
            if(globalsfile==null || !globalsfile.exists()){
                System.out.println(Repository.GLOBALSREMOTEFILE+" could not be opened localy");
                return;
            }
            doc = db.parse(globalsfile);
            doc.getDocumentElement().normalize();  
        } catch(Exception e){
            e.printStackTrace();
        }
    }

    public void init(){
        root = new DefaultMutableTreeNode("root", true);
        tree = new JTree(root);
        tree.setRootVisible(false);
        tree.setCellRenderer(new CustomIconRenderer());
        panel = new JScrollPane(tree);
        
        tree.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(ev.getKeyCode()==KeyEvent.VK_DELETE){
                    TreePath []tps = tree.getSelectionPaths();
                    for(TreePath pth:tps){
                        DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)pth.getLastPathComponent();
                        Object myObj = treenode.getUserObject();
                        if( myObj instanceof MyFolder){
                            try{removeFolder((MyFolder)myObj, treenode,false);}
                            catch(Exception e){e.printStackTrace();}
                        } else if(myObj instanceof MyParam){
                            try{removeParam((MyParam)myObj, treenode,false);}
                            catch(Exception e){e.printStackTrace();}
                        }
                    }
                    writeXML();
                    uploadFile();
                }
            }
        });
        
        tree.addMouseListener(new MouseAdapter(){
            public void mouseReleased(MouseEvent ev){
                TreePath tp = tree.getPathForLocation(ev.getX(), ev.getY());
                if (tp != null){
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        tree.setSelectionPath(tp);
                        if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof MyFolder){
                            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            MyFolder folder = (MyFolder)treenode.getUserObject();
                            showFolderPopUp(treenode,ev,folder);
                        }else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof MyParam){
                            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            MyParam param = (MyParam)treenode.getUserObject();
                            showParamPopUp(treenode,ev,param);
                        }
                    }
                } else {
                    tree.setSelectionPath(null);
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        showNewFolderPopUp(ev);
                    } 
                }
            }
        }
        );
    }
    
    public void showNewFolderPopUp(MouseEvent ev){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Add Folder");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addFolder();}});
        p.add(item);
        p.show(this.tree,ev.getX(),ev.getY());
    }
    
    public void addFolder(){
        String resp = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, 
                                                    panel, "Name", "Folder name: ");
        if(resp!=null&&!resp.equals("")){
            try{
                Element rootElement = doc.createElement("folder");
                
                doc.getFirstChild().appendChild(rootElement);
                Element fname = doc.createElement("fname");
                rootElement.appendChild(fname);  
                Node node = doc.createTextNode(resp);
                fname.appendChild(node);
                
                MyFolder folder = new MyFolder(node);
                
                DefaultMutableTreeNode temp = new DefaultMutableTreeNode(folder,true);
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, root,root.getChildCount());
                
                writeXML();
                uploadFile();
                
            } catch(Exception e){
                e.printStackTrace();
            }
        }
    }
    
    /*
     * popup user on Node
     * right click
     */
    public void showParamPopUp(final DefaultMutableTreeNode treenode,MouseEvent ev,final MyParam node){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Change param");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                changeParam(treenode,node);}});
        p.add(item);
        item = new JMenuItem("Remove param");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                removeParam(node,treenode,true);}});
        p.add(item);
        p.show(this.tree,ev.getX(),ev.getY());
    }
    
    /*
     * remove parameter
     */
    public void removeParam(MyParam node,DefaultMutableTreeNode treenode,boolean refresh){
        ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(treenode);
        Node child = node.getValue().getParentNode().getParentNode();
        child.getParentNode().removeChild(child);
        if(refresh){
            writeXML();
            uploadFile();
        }
    }
    
    /*
     * change parameter node
     */
    public void changeParam(DefaultMutableTreeNode treenode,MyParam node){  
        JTextField name = new JTextField();   
        name.setText(node.getName().getNodeValue());
        JTextField value = new JTextField();
        value.setText(node.getValue().getNodeValue());
        JPanel p = getPropPanel(name,value);
        int r = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE, 
                                                JOptionPane.OK_CANCEL_OPTION, 
                                                panel, "Property: value",null);
        if(r == JOptionPane.OK_OPTION&&(!(name.getText()+value.getText()).equals(""))){
            node.getName().setNodeValue(name.getText());
            node.getValue().setNodeValue(value.getText());
            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
            writeXML();
            uploadFile();
        }
    }
    
    
    /*
     * name value panel created
     * for adding props
     */        
    public JPanel getPropPanel(JTextField name, JTextField value){
        JPanel p = new JPanel();
        p.setLayout(new BoxLayout(p, BoxLayout.Y_AXIS));
        
        JLabel jLabel3 = new JLabel();
        JPanel jPanel1 = new JPanel();
        jPanel1.setLayout(new java.awt.BorderLayout());
        jLabel3.setText("Name: ");
        jPanel1.add(jLabel3, BorderLayout.CENTER);
        p.add(jPanel1);
        p.add(name);
        
        if(value!=null){
            JPanel jPanel2 = new JPanel();
            JLabel jLabel4 = new JLabel();
            jPanel2.setLayout(new BorderLayout());
            jLabel4.setText("Value: ");
            jPanel2.add(jLabel4, BorderLayout.CENTER);
            p.add(jPanel2);
            p.add(value);
        }
        return p;}
    
    /*
     * popup user on Node
     * right click
     */
    public void showFolderPopUp(final DefaultMutableTreeNode treenode,MouseEvent ev,final MyFolder node){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Rename folder");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                renameFolder(treenode,node);}});
        p.add(item);
        item = new JMenuItem("Append folder");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                appendFolder(treenode,node);}});
        p.add(item);
        item = new JMenuItem("Append param");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                appendParam(treenode,node);}});
        p.add(item);
        item = new JMenuItem("Remove folder");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                removeFolder(node,treenode,true);}});
        p.add(item);
        p.show(this.tree,ev.getX(),ev.getY());
    }
    
    public void renameFolder(DefaultMutableTreeNode treenode, MyFolder parent){
        JTextField name = new JTextField();   
        name.setText(parent.toString());
        
        JPanel p = getPropPanel(name,null);
        int r = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE, 
                                                JOptionPane.OK_CANCEL_OPTION, 
                                                panel, "Folder name",null);
        if(r == JOptionPane.OK_OPTION&&(!name.getText().equals(""))){
            //node.getName().setNodeValue(name.getText());
            parent.getNode().setNodeValue(name.getText());
            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
            writeXML();
            uploadFile();
        }
    }
        
    /*
     * create and append new node 
     * to this parent node
     */
    public void appendParam(DefaultMutableTreeNode treenode, MyFolder parent){
        
        JTextField name = new JTextField();
        JTextField value = new JTextField();
        JPanel p = getPropPanel(name,value);
        int r = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE, 
                                                JOptionPane.OK_CANCEL_OPTION, 
                                                panel, "Property: value",null);
        if(r == JOptionPane.OK_OPTION&&(!(name.getText()+value.getText()).equals(""))){
            
            MyParam param = new MyParam();
            
            Element rootElement = doc.createElement("param");
            parent.getNode().getParentNode().getParentNode().appendChild(rootElement);
            
            Node refs = null;
            try{refs = parent.getNode().getParentNode().getParentNode().getFirstChild().getNextSibling().getNextSibling().getNextSibling();}
            catch(Exception e){refs=null;}
            if(refs==null){
                parent.getNode().getParentNode().getParentNode().appendChild(rootElement);
            } else {
                parent.getNode().getParentNode().getParentNode().insertBefore(rootElement, refs);
            }
            
            Element tname = doc.createElement("name");
            rootElement.appendChild(tname);  
            Node node = doc.createTextNode(name.getText());
            param.setName(node);
            tname.appendChild(node);
            
            Element tvalue = doc.createElement("value");
            rootElement.appendChild(tvalue);  
            node = doc.createTextNode(value.getText());
            param.setValue(node);
            tvalue.appendChild(node);
            
            DefaultMutableTreeNode temp = new DefaultMutableTreeNode(param,true);
            ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treenode,0);
            
            writeXML();
            uploadFile();
        }
    }
    
    
    /*
     * create and append new node 
     * to this parent node
     */
    public void appendFolder(DefaultMutableTreeNode treenode, MyFolder parent){
        String resp = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, 
                                                    panel, "Name", "Folder name: ");
        if(resp!=null&&!resp.equals("")){
            Element rootElement = doc.createElement("folder");
            parent.getNode().getParentNode().getParentNode().appendChild(rootElement);
            Element fname = doc.createElement("fname");
            rootElement.appendChild(fname);  
            Node node = doc.createTextNode(resp);
            fname.appendChild(node);
            MyFolder folder = new MyFolder(node);
            
            DefaultMutableTreeNode temp = new DefaultMutableTreeNode(folder,true);
            ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treenode,treenode.getChildCount());
            
            writeXML();
            uploadFile();
        }
    }
    
    /*
     * remove node
     */
    public void removeFolder(MyFolder node,DefaultMutableTreeNode treenode, boolean refresh){
        ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(treenode);
        Node child = node.getNode().getParentNode().getParentNode();
        child.getParentNode().removeChild(child);
        if(refresh){
            writeXML();
            uploadFile();
        }
    }
    
    public File getGlobalsFile(){
        File file = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+"config"+Repository.getBar()+"globals.xml");
        try{InputStream in = Repository.c.get(Repository.GLOBALSREMOTEFILE);
            InputStreamReader inputStreamReader = new InputStreamReader(in);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            BufferedWriter writer = null;
            String line;
            try{writer = new BufferedWriter(new FileWriter(file));
                while ((line=bufferedReader.readLine())!= null){
                    writer.write(line);
                    writer.newLine();}
                bufferedReader.close();
                writer.close();
                inputStreamReader.close();
                in.close();
                System.out.println("successfull");}
            catch(Exception e){
                e.printStackTrace();
                return file;
            }
        }
        catch(Exception e){
            e.printStackTrace();
            System.out.println("Could not get :"+
                                Repository.GLOBALSREMOTEFILE+" as globals param file");
            return file;
        }
        return file;
    }
        
    public void buildTree(){
        ((DefaultMutableTreeNode)tree.getModel().getRoot()).removeAllChildren();        
        try{xpath = XPathFactory.newInstance().newXPath();
            XPathExpression expr1 = xpath.compile("//root/folder");
            NodeList nodes = (NodeList)expr1.evaluate(doc, XPathConstants.NODESET);
            for(int i=0;i<nodes.getLength();i++){
                parseFolder(nodes.item(i),root);
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
        ((DefaultTreeModel)tree.getModel()).reload();
    }
    
    public void parseFolder(Node node,DefaultMutableTreeNode parent){
        try{
            Node n = ((Element)node).getElementsByTagName("fname").item(0);
            //String fname = n.getFirstChild().getNodeValue();
            MyFolder fname = new MyFolder(n.getFirstChild());
            DefaultMutableTreeNode temp = new DefaultMutableTreeNode(fname,true);
            parent.add(temp);
            XPathExpression expr1 = xpath.compile("param");
            NodeList nodes = (NodeList)expr1.evaluate(node, XPathConstants.NODESET);
            for(int i=0;i<nodes.getLength();i++){
                MyParam param = new MyParam();
                n = ((Element)nodes.item(i)).getElementsByTagName("name").item(0);
                //String name = n.getFirstChild().getNodeValue();
                param.setName(n.getFirstChild());
                n = ((Element)nodes.item(i)).getElementsByTagName("value").item(0);
                //String value = n.getFirstChild().getNodeValue();
                param.setValue(n.getFirstChild());
                temp.add(new DefaultMutableTreeNode(param,true));
            }
            expr1 = xpath.compile("folder");
            nodes = (NodeList)expr1.evaluate(node, XPathConstants.NODESET);
            for(int i=0;i<nodes.getLength();i++){
                parseFolder(nodes.item(i),temp);
            }
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
    public void writeXML(){
        try{
            DOMSource source = new DOMSource(doc);                    
            Result result = new StreamResult(globalsfile);
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            transformer.transform(source, result);
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
    private void uploadFile(){
        try{StringBuilder path = new StringBuilder();
            String[] globalsremote = Repository.GLOBALSREMOTEFILE.split("/");
            String filename = globalsremote[globalsremote.length-1];
            globalsremote[globalsremote.length-1]="";
            for(String s:globalsremote){
                path.append("/");
                path.append(s);
            }
            path.delete(0, 1);
            String location = path.toString();
            FileInputStream in = new FileInputStream(globalsfile);
            try{
                while(!finished){
                    try{Thread.sleep(100);}
                    catch(Exception e){e.printStackTrace();}
                }
                finished = false;
                ch.cd(location);
                ch.put(in, filename);
                in.close();
                finished = true;}
            catch(Exception e){
                e.printStackTrace();
                finished = true;
            }
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    
    /*
     * initialize SFTP connection used
     * for plugins and configuration files transfer
     */
    public void initSftp(){
        try{
            JSch jsch = new JSch();
            Session session = jsch.getSession(Repository.user, Repository.host, 22);
            session.setPassword(Repository.password);
            Properties config = new Properties();
            config.put("StrictHostKeyChecking", "no");
            session.setConfig(config);
            session.connect();
            Channel channel = session.openChannel("sftp");
            channel.connect();
            ch = (ChannelSftp)channel;
        } catch (Exception e){
            System.out.println("ERROR: Could not initialize SFTP for plugins");
            e.printStackTrace();
        }
    }
}