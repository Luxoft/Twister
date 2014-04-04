/*
File: SutEditor.java ; This file is part of Twister.
Version: 2.016

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
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTree;
import java.awt.BorderLayout;
import java.util.List;
import java.util.ArrayList;
import java.awt.datatransfer.UnsupportedFlavorException;
import javax.swing.tree.TreeNode;
import java.awt.datatransfer.Transferable;
import javax.swing.JComponent;
import java.awt.datatransfer.DataFlavor;
import javax.swing.TransferHandler;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreePath;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.DropMode;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JTextField;
import java.awt.Dimension;
import javax.swing.event.TreeSelectionListener;
import javax.swing.event.TreeSelectionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JOptionPane;
import com.twister.CustomDialog;
import javax.swing.tree.TreeSelectionModel;
import java.util.HashMap;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.net.URL;
import java.util.Set;
import java.util.Iterator;
import javax.swing.JList;
import javax.swing.DefaultComboBoxModel;
import java.util.Arrays;
import java.util.Enumeration;
import java.awt.event.KeyEvent;
import java.awt.event.KeyAdapter;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import com.twister.MySftpBrowser;
import java.awt.Container;
import javax.swing.AbstractAction;
import java.awt.event.HierarchyListener;
import java.awt.event.HierarchyEvent;
import javax.swing.BorderFactory;
import javax.swing.JSplitPane;
import java.util.Vector;
import java.util.Collections;
import java.util.Properties;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.SwingUtilities;
import java.awt.Color;
import javax.swing.DefaultListModel;

public class SutEditor extends JPanel{
    private JTree tree;
    private XmlRpcClient client;
    public DefaultMutableTreeNode root;
    private JButton saveas,redcomp,addcomp,save,close,setep;
    private JLabel jusers;
    private SutTree suttree;
    private String rootsut;
    public DefaultMutableTreeNode sutnode;
    private boolean lastsaved = true;
    private boolean editable;
    public JScrollPane sp;

    public SutEditor(){
        suttree = new SutTree();
        initializeRPC();
        
        tree = new JTree();
        tree.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(ev.getKeyCode()==KeyEvent.VK_C && ev.isControlDown()){
                    if(tree.getSelectionPath()==null){return;}
                    String s = tree.getSelectionPath().getLastPathComponent().toString();
                    s = s.replace("EP:","");
                    s = s.replace("ID:","");
                    s = s.replace("Path:","");
                    StringSelection selection = new StringSelection(s);
                    Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
                    clipboard.setContents(selection, selection);
                }
            }});
        tree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
        root = new DefaultMutableTreeNode("root");        
        DefaultTreeModel treemodel = new DefaultTreeModel(root,true);
        tree.setModel(treemodel);
        tree.setDragEnabled(true);
        tree.setRootVisible(false);
        tree.setDropMode(DropMode.ON_OR_INSERT);
        if(PermissionValidator.canChangeSut()){
            tree.setTransferHandler(new ImportTreeTransferHandler());
            tree.setDragEnabled(true);
        }
        tree.setCellRenderer(new CustomIconRenderer());
        setLayout(new BorderLayout());
        sp = new JScrollPane(tree);
        final JSplitPane splitpane = new JSplitPane();
        JPanel bottompanel = new JPanel();        
        bottompanel.setLayout(new BorderLayout());
        bottompanel.add(sp,BorderLayout.CENTER);
        splitpane.setRightComponent(bottompanel);
        splitpane.setLeftComponent(suttree);
        splitpane.setResizeWeight(0.5);
        splitpane.setOrientation(JSplitPane.VERTICAL_SPLIT);
        add(splitpane,BorderLayout.CENTER);
        JPanel sutopt = new JPanel();
        JPanel filesoption = new JPanel();
        
        setep = new JButton("Set EP");
        setep.setEnabled(false);
        setep.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                JPanel p = new JPanel();
                p.setLayout(null);
                p.setPreferredSize(new Dimension(250,200));
                JLabel epl = new JLabel("Run on EP's: ");
                epl.setBounds(5,35,80,25);
                JList tep = new JList();
                JScrollPane scep = new JScrollPane(tep);
                scep.setBounds(90,35,155,150);
                p.add(epl);
                p.add(scep);
                suttree.populateEPs(tep,null);
                String []  eps = ((DefaultMutableTreeNode)root.getFirstChild()).getUserObject().toString().replace("EP:", "").split(";");
                Object [] ob = ((DefaultListModel)tep.getModel()).toArray();
                int size = ob.length;
                ArrayList array = new ArrayList();
                for(String ep:eps){
                    for(int i=0;i<size;i++){
                        if(ob[i].toString().equals(ep)){
                            array.add(i);
                        }
                    }
                }
                int [] indices = new int[array.size()];
                for(int i = 0;i<array.size();i++){
                    indices[i] = (Integer)array.get(i);
                }
                tep.setSelectedIndices(indices);
                
                int resp = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE, 
                            JOptionPane.OK_CANCEL_OPTION, SutEditor.this, "Select EP",null);
                if(resp == JOptionPane.OK_OPTION){
                    try{
                        StringBuilder sb = new StringBuilder();
                        for(int i=0;i<tep.getSelectedValuesList().size();i++){
                            sb.append(tep.getSelectedValuesList().get(i).toString());
                            sb.append(";");
                        }
                        String query = "{'_epnames_"+RunnerRepository.user+"':'"+sb.toString()+"'}";
                        query = client.execute("setSut", new Object[]{"/"+rootsut,"/",query,RunnerRepository.user}).toString();
                        if(query.indexOf("ERROR")==-1){
                           ((DefaultMutableTreeNode)root.getFirstChild()).setUserObject("EP:"+sb.toString());
                           ((DefaultTreeModel)tree.getModel()).nodeChanged(root.getFirstChild());
                           lastsaved = false;
                        } else {
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutEditor.this,"ERROR", query);
                        }
                    }
                    catch(Exception e){
                        e.printStackTrace();
                    }   
                }
            }});
        addcomp = new JButton("Add Component");
        addcomp.setEnabled(false);
        addcomp.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                String name = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, 
                                                    SutEditor.this, "Name", "Component name: ");
                if(name!=null&&!name.equals("")){
                    TreePath tp = tree.getSelectionPath();
                    DefaultMutableTreeNode treenode;
                    if(tp==null){
                        treenode = root;
                    } else {
                        treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                    }
                    if(checkExistingName(treenode, name, null)){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,SutEditor.this,"Warning", 
                                        "This name is already used, please use different name.");
                        return;
                    }
                    String parent = "";
                    if(tp==null){
                        parent = "/"+rootsut;
                    } else {
                        parent = treenode.getFirstChild().toString().split("ID: ")[1];
                    }
                    try{
                        String resp = client.execute("setSut", new Object[]{name,parent,"",RunnerRepository.user}).toString();
                        if(resp.indexOf("ERROR")==-1){
                            Comp comp = new Comp(name,resp,"");
                            DefaultMutableTreeNode component = new DefaultMutableTreeNode(comp,true);
                            DefaultMutableTreeNode id = new DefaultMutableTreeNode("ID: "+resp,false);
                            component.add(id);
                            ((DefaultTreeModel)tree.getModel()).insertNodeInto(component, treenode, treenode.getChildCount());
                            lastsaved = false;
                        } else {
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutEditor.this,"ERROR", resp);
                        }
                    } catch (Exception e){
                        System.out.println("Could not send command to add component to server");
                        e.printStackTrace();
                    }
                }
            }
        });
        
        redcomp = new JButton("Delete Component");
        redcomp.setEnabled(false);
        redcomp.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                TreePath tp = tree.getSelectionPath();
                if(tp==null||tp.getPathCount()==0)return;
                DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                try{
                    String torem = "";// "/"+treenode.toString();
                    Object userobj = treenode.getUserObject();
                    if(userobj instanceof Node){
                        DefaultMutableTreeNode parent = (DefaultMutableTreeNode)treenode.getParent();
                        Comp comp = (Comp)parent.getUserObject();
                        String parentid = comp.getName();
                        String name="";
                        if(parent.getLevel()==1){
                            name = "/"+rootsut;
                        } else {
                            name = ((Comp)((DefaultMutableTreeNode)parent.getParent()).getUserObject()).getID();
                        }
                        HashMap <String,String>hm = new <String,String>HashMap();
                        hm.put("_id","");
                        System.out.println(parentid+" - "+name+" - "+hm.toString()+" - "+RunnerRepository.user);
                        String resp = client.execute("setSut", new Object[]{parentid,name,hm,RunnerRepository.user}).toString();
                        if(resp.indexOf("ERROR")==-1){
                            DefaultTreeModel model = (DefaultTreeModel)tree.getModel();
                            model.removeNodeFromParent(treenode);
                        }
                        else{
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutEditor.this,"ERROR", resp);
                        }
                    } else if (userobj instanceof Comp) {
                        torem = ((Comp)userobj).getID();
                        String s = client.execute("deleteSut", new Object[]{torem,RunnerRepository.user}).toString();
                        if(s.indexOf("ERROR")==-1){
                        ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(treenode);
                        selectedSUT(null);                        
                        if(!(userobj instanceof Node)&&!(userobj instanceof Comp)){
                            RunnerRepository.window.mainpanel.p1.suitaDetails.setComboTBs();
                        }
                            lastsaved = false;
                        } else {
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutEditor.this,"Error", s);
                        }
                    }
                } catch (Exception e){
                    e.printStackTrace();
                }
            }
        });
        
        save = new JButton("Save");
        save.setEnabled(false);
        save.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                try{String resp = client.execute("saveReservedSut", new Object[]{"/"+rootsut,RunnerRepository.user}).toString();
                    if(resp.indexOf("ERROR")!=-1){
                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutEditor.this,"ERROR", resp);
                    }
                    lastsaved = true;
                }
                catch(Exception e){e.printStackTrace();}
            };
        });
        
        saveas = new JButton("Save As");
        saveas.setEnabled(false);
        saveas.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                String filename = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE,
                                     JOptionPane.OK_CANCEL_OPTION
                                     ,SutEditor.this,
                                     "Sut Name", "Please enter sut name");
                if(filename!=null&&!filename.equals("NULL")){
                    try{String resp = client.execute("saveReservedSutAs", new Object[]{filename,"/"+rootsut,RunnerRepository.user}).toString();
                        if(resp.indexOf("ERROR")!=-1){
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutEditor.this,"ERROR", resp);
                        }
                        close.doClick();
                        SUT s = new SUT(filename,".user");
                        sutnode = new DefaultMutableTreeNode(s,false);
                        suttree.addUserNode(sutnode);
                        if(suttree.reserveSut(s)){
                            s.setReserved(RunnerRepository.user);
                            ((DefaultTreeModel)suttree.filestree.getModel()).nodeChanged(sutnode);
                            getSUT(filename+".user",sutnode,true);
                        }
                    } catch (Exception e){
                        e.printStackTrace();
                    }
                }
                
            };
        });
        close  = new JButton("Close");
        close.setEnabled(false);
        close.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(editable){
                    String resp = "";
                    try{
                        if(lastsaved){
                            resp = client.execute("discardAndReleaseReservedSut", new Object[]{"/"+rootsut,RunnerRepository.user}).toString();
                        } else {
                            String[] buttons = {"Save","Discard"};
                            resp = CustomDialog.showButtons(SutEditor.this, JOptionPane.QUESTION_MESSAGE,
                                                                    JOptionPane.DEFAULT_OPTION, null,buttons ,
                                                                    "Save","Save SUT before closing?");
                            if (!resp.equals("NULL")) {
                                if(resp.equals("Save")){
                                    resp = client.execute("saveAndReleaseReservedSut", new Object[]{"/"+rootsut,RunnerRepository.user}).toString();
                                }
                                else if(resp.equals("Discard")){
                                    resp = client.execute("discardAndReleaseReservedSut", new Object[]{"/"+rootsut,RunnerRepository.user}).toString();
                                }
                            } else {
                                resp = client.execute("discardAndReleaseReservedSut", new Object[]{"/"+rootsut,RunnerRepository.user}).toString();
                            }
                        }
                        if(resp.indexOf("*ERROR*")!=-1){
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutEditor.this,"ERROR", resp);
                        }
                    }
                    catch(Exception e){e.printStackTrace();}
                    suttree.releaseSut(rootsut);
                }
                rootsut = "";
                root.removeAllChildren();
                addcomp.setEnabled(false);
                close.setEnabled(false);
                setep.setEnabled(false);
                save.setEnabled(false);
                saveas.setEnabled(false);
                redcomp.setEnabled(false);
                ((DefaultTreeModel)tree.getModel()).reload();
                lastsaved = true;
            };
        });
        if(PermissionValidator.canChangeSut()){
            sutopt.add(addcomp);
            sutopt.add(redcomp);
            sutopt.add(setep);
            sutopt.add(save);
            sutopt.add(saveas);
            sutopt.add(close);
        }
        bottompanel.add(sutopt,BorderLayout.SOUTH);     
        tree.addTreeSelectionListener(new TreeSelectionListener(){
            public void valueChanged(TreeSelectionEvent ev){                
                TreePath newPath = ev.getNewLeadSelectionPath();                 
                DefaultMutableTreeNode newNode = null;  
                if(newPath != null){
                    newNode = (DefaultMutableTreeNode)newPath.getLastPathComponent();
                    selectedSUT(newNode);
                } else {
                    selectedSUT(null);
                }
            }
        });
        tree.addMouseListener(new MouseAdapter(){
            public void mouseReleased(MouseEvent ev){
                int row=tree.getRowForLocation(ev.getX(),ev.getY());  
                if(row==-1) tree.clearSelection();  
            }});
    }

    /*
     * checking existing name in structure
     * name - the name to search for
     * parent - the parent in which children to search
     * current - the node to ommit on search
     */
    
    public boolean checkExistingName(DefaultMutableTreeNode parent, String name, DefaultMutableTreeNode current){
        Enumeration e = parent.children();
        while(e.hasMoreElements()){
            DefaultMutableTreeNode child = (DefaultMutableTreeNode)e.nextElement();
            if(child!=current){
                if(child.getUserObject() instanceof String){
                    if(name.equals(child.toString())){
                        return true;
                    }
                } else if(child.getUserObject() instanceof SUT){
                    String childname = ((SUT)child.getUserObject()).getName();
                    if(name.equals(childname)){
                        return true;
                    }
                } else if(child.getUserObject() instanceof Comp){
                    String childname = ((Comp)child.getUserObject()).getName();
                    if(name.equals(childname)){
                        return true;
                    }
                }
            }
            
        }
        return false;
    }

    public JTree getTree(){
        return this.tree;
    }
    
    public void closeSut(){
        if(close.isEnabled()){
            close.doClick();
        }
    }
    
    private void selectedSUT(DefaultMutableTreeNode newNode){
        if(editable){
            if(newNode!=null){
                if(newNode.getUserObject()  instanceof Comp){
                    addcomp.setEnabled(true);
                    redcomp.setEnabled(true);
                } else {
                    addcomp.setEnabled(false);
                    redcomp.setEnabled(true);
                }        
            } else{
                redcomp.setEnabled(false);
                addcomp.setEnabled(true);
            }
        }
    }
    
    public void getSUT(String sutname,DefaultMutableTreeNode sutnode,boolean editable){
        try{
            Object ob = client.execute("getSutByName", new Object[]{sutname,RunnerRepository.user});
            HashMap hash = (HashMap)ob;
            this.editable = editable;
            DefaultMutableTreeNode epsnode;//child
            DefaultTreeModel model = (DefaultTreeModel)tree.getModel();
            root.removeAllChildren();
            String name,path,eps;
            Object[] subchildren;
                path = hash.get("path").toString();
                name = path.split("/")[path.split("/").length-1];
                try{eps = ((HashMap)hash.get("meta")).get("_epnames_"+RunnerRepository.user).toString();}
                catch(Exception e){eps = "";}
                epsnode = new DefaultMutableTreeNode("EP:"+eps,false);
                root.add(epsnode);
                subchildren = (Object[])hash.get("children");
                buildChildren(subchildren,root);
            model.reload();
            this.rootsut = sutname;
            this.sutnode = sutnode;
            if(editable){
                addcomp.setEnabled(true);
                save.setEnabled(true);
                saveas.setEnabled(true);
                close.setEnabled(true);
                setep.setEnabled(true);
                lastsaved = true;
            } else {
                addcomp.setEnabled(false);
                save.setEnabled(false);
                saveas.setEnabled(false);
                close.setEnabled(true);
                setep.setEnabled(false);
                lastsaved = true;
            }
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    
    
    private void buildChildren(Object [] children, DefaultMutableTreeNode treenode){
        String childid, subchildid;
        for(Object o:children){
            try{
                HashMap subhash= (HashMap)o;
                String subpath = subhash.get("path").toString();
                String subname = subpath.split("/")[subpath.split("/").length-1];
                HashMap meta = (HashMap)subhash.get("meta");
                String id = subhash.get("id").toString();
                Comp comp = new Comp(subname,id,meta.get("_id")+"");
                DefaultMutableTreeNode component = new DefaultMutableTreeNode(comp,true);
                DefaultMutableTreeNode nodeid = new DefaultMutableTreeNode("ID: "+id,false);
                component.add(nodeid);
                treenode.add(component);
                if(meta.get("_id")!=null){
                    String referenceid = meta.get("_id").toString();
                    Node child = getTB(referenceid,null);
                    DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(child);
                    DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+child.getID(),false);
                    treechild.add(temp);
                    DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(child.getPath(),false);
                    treechild.add(temp2);
                    ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, component,component.getChildCount());
                }
                Object [] subchildren = (Object[])subhash.get("children");
                buildChildren(subchildren,component);
            } catch (Exception e){
                e.printStackTrace();
            }
        }
    }
    
    /*
     * create a node based om an id
     * the node is created from the data 
     * received from server
     */
    public Node getTB(String id,Node parent){
        Object resp = null;
        try{
            resp = client.execute("getResource", new Object[]{id});
            HashMap hash= (HashMap)resp;
            String path = hash.get("path").toString();
            String name = path.split("/")[path.split("/").length-1];
            byte type = 1;
            if(path.indexOf("/")==-1){
                type = 0;
            }
            Node node = new Node(id,path,name,parent,null,type);
            Object[] children = (Object[])hash.get("children");
            for(Object o:children){
                node.addChild(o.toString(), null);
            }
            HashMap meta = (HashMap)hash.get("meta");
            if(meta!=null&&meta.size()!=0){
                Set keys = meta.keySet();
                Iterator iter = keys.iterator();
                while(iter.hasNext()){
                    String n = iter.next().toString();
                    if(n.equals("_epnames_"+RunnerRepository.user)){
                        node.setEPs(meta.get(n).toString());
                        continue;
                    }
                    node.addProperty(n, meta.get(n).toString());
                }
            }
            return node;
        }catch(Exception e){
            System.out.println("server respons: "+resp.toString());
            e.printStackTrace();
            return null;
        }
    }
    
    public SutTree getSutTree(){
        return suttree;
    }
    
    public void setRootSutName(String rootsut){
        this.rootsut = rootsut;
    }
    
    public String getEpsFromSut(String sutname){
        String eps = "";
        try{HashMap hash= (HashMap)client.execute("getSut", new Object[]{sutname,RunnerRepository.user,RunnerRepository.user});
            try{eps = ((HashMap)hash.get("meta")).get("_epnames_"+RunnerRepository.user).toString();}
            catch(Exception e){
                //System.out.println("Error in getting _epnames_"+RunnerRepository.user+" from meta in: "+hash.toString()+" . Called in SutEditor->getEpsFromSut");
                eps = "";
            }
        }
        catch(Exception e){
            eps = "";
            e.printStackTrace();
        }
        System.out.println(sutname+" has "+eps);
        return eps;
    }
    
    /*
     * initialize RPC connection
     * based on host an port of 
     * resource allocator specified in config
     */
    public void initializeRPC(){
        try{XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
            configuration.setServerURL(new URL("http://"+RunnerRepository.host+
                                        ":"+RunnerRepository.getCentralEnginePort()+"/ra/"));
            configuration.setEnabledForExtensions(true);
            configuration.setBasicPassword(RunnerRepository.password);
            configuration.setBasicUserName(RunnerRepository.user);
            client = new XmlRpcClient();
            client.setConfig(configuration);
            System.out.println("XMLRPC Client for SutEditor initialized: "+client);}
        catch(Exception e){System.out.println("Could not conect to "+
                            RunnerRepository.host+" :"+RunnerRepository.getCentralEnginePort()+"/ra/"+
                            "for RPC client initialization");}
    }
    
    class ImportTreeTransferHandler extends TransferHandler {  
    
    
        DataFlavor nodesFlavor;  
        DataFlavor[] flavors = new DataFlavor[1];
       
        public ImportTreeTransferHandler() {  
            try {  
                String mimeType = DataFlavor.javaJVMLocalObjectMimeType +  
                                  ";class=\"" +  
                                  Node.class.getName() +  
                                  "\"";  
                nodesFlavor = new DataFlavor(mimeType);  
                flavors[0] = nodesFlavor;  
            } catch(ClassNotFoundException e) {  
                System.out.println("ClassNotFound: " + e.getMessage());  
            }  
        }  
       
        public boolean canImport(TransferHandler.TransferSupport support) {  
            if(!editable)return false;
            if(!support.isDrop()) {  
                return false;  
            }  
            support.setShowDropLocation(true);  
            if(!support.isDataFlavorSupported(nodesFlavor)) {  
                return false;  
            }  
            JTree.DropLocation dl = (JTree.DropLocation)support.getDropLocation(); 
            TreePath dest = dl.getPath();  
            DefaultMutableTreeNode target = (DefaultMutableTreeNode)dest.getLastPathComponent(); 
            if(!(target.getUserObject() instanceof Comp)){
                return false;
            }
            Node[] nodes = null; 
            try{Transferable t = support.getTransferable();  
                nodes = (Node[])t.getTransferData(nodesFlavor);
                Enumeration e;
                Node node=null;
                for(Node n:nodes){
                    if(target.getLevel()==1){
                        e = target.children();
                        while(e.hasMoreElements()){
                            Object ob= ((DefaultMutableTreeNode)e.nextElement()).getUserObject();
                            if(!(ob instanceof Node))continue;
                            node = (Node)ob;
                            if(n.getID().equals(node.getID())){
                                return false;
                            }
                        }
                    }
                }
            } catch (Exception e){
                e.printStackTrace();
            }
            return true;  
        }
         
        private DefaultMutableTreeNode copy(TreeNode node) {  
            return new DefaultMutableTreeNode(node);  
        }  
       
        public int getSourceActions(JComponent c) {  
            return COPY;  
        }  
       
        public boolean importData(TransferHandler.TransferSupport support) {  
            try{
                if(!canImport(support)) {  
                    return false;  
                }
                Node[] nodes = null;  
                try {  
                    Transferable t = support.getTransferable();  
                    nodes = (Node[])t.getTransferData(nodesFlavor);  
                } catch(UnsupportedFlavorException ufe) {  
                    System.out.println("UnsupportedFlavor: " + ufe.getMessage());  
                } catch(java.io.IOException ioe) {  
                    System.out.println("I/O error: " + ioe.getMessage());  
                }
                JTree.DropLocation dl = (JTree.DropLocation)support.getDropLocation();  
                TreePath dest = dl.getPath();  
                DefaultMutableTreeNode parent = (DefaultMutableTreeNode)dest.getLastPathComponent();
                JTree tree = (JTree)support.getComponent();  
                DefaultTreeModel model = ((DefaultTreeModel)tree.getModel());  
                if(parent.getChildCount()>1){//removes previously added tb's
                    for(int i=0;i<parent.getChildCount();i++){
                        if(((DefaultMutableTreeNode)parent.getChildAt(i)).getUserObject() instanceof Node){
                            model.removeNodeFromParent((DefaultMutableTreeNode)parent.getChildAt(i));
                        }
                    }
                }
                int index = parent.getChildCount();  
                for(int i = 0; i < nodes.length; i++){ 
                    try{
                        String id = "";
                        if(nodes[i].getType()==0){
                            try{System.out.println("getresource: "+"/"+nodes[i].getName());
                                HashMap hash = (HashMap)client.execute("getResource", new Object[]{"/"+nodes[i].getName()});
                                id = hash.get("id").toString();
                            } catch(Exception e){
                                e.printStackTrace();
                                id = "/"+nodes[i].getName();
                            }
                        } else {
                            id = nodes[i].getID();
                        }
                        Comp comparent = (Comp)parent.getUserObject();
                        HashMap <String,String>hm = new <String,String>HashMap();
                        hm.put("_id", id);
                        String parentid="";
                        parentid = ((Comp)(parent.getUserObject())).getName();
                        String name = "";
                        if(parent.getLevel()==1){
                            name = "/"+rootsut;
                        } else {
                            name = ((Comp)((DefaultMutableTreeNode)parent.getParent()).getUserObject()).getID();
                        }
                        System.out.println(parentid+" - "+name+" - "+hm.toString()+" - "+RunnerRepository.user);
                        String resp = client.execute("setSut", new Object[]{parentid,name,hm,RunnerRepository.user}).toString();
                        
                        if(resp.indexOf("ERROR")==-1){
                            DefaultMutableTreeNode element = createChildren(nodes[i]);
                            model.insertNodeInto(element, parent, 1);
                        }
                        else{
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,SutEditor.this,"ERROR", resp);
                        }
                    } catch (Exception e){
                        e.printStackTrace();
                    }
                    
                } 
                lastsaved = false;
                return true; 
            } catch(Exception e){
                e.printStackTrace();
                return false;
            }
        } 
        
        private DefaultMutableTreeNode createChildren(Node node){
            DefaultMutableTreeNode parent = new DefaultMutableTreeNode(node);            
            DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+node.getID(),false);
            parent.add(temp);            
            temp = new DefaultMutableTreeNode(node.getPath(),false);
            parent.add(temp);            
            return parent;
        }
       
        public String toString() {  
            return getClass().getName();  
        }  
       
        public class NodesTransferable implements Transferable {  
            DefaultMutableTreeNode[] nodes;  
       
            public NodesTransferable(DefaultMutableTreeNode[] nodes) {  
                this.nodes = nodes;  
             }  
       
            public Object getTransferData(DataFlavor flavor)  
                                     throws UnsupportedFlavorException {  
                if(!isDataFlavorSupported(flavor))  
                    throw new UnsupportedFlavorException(flavor);  
                return nodes;  
            }  
       
            public DataFlavor[] getTransferDataFlavors() {  
                return flavors;  
            }  
       
            public boolean isDataFlavorSupported(DataFlavor flavor) {  
                return nodesFlavor.equals(flavor);  
            }  
        }  
    }
}