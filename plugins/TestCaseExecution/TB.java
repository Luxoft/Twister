/*
File: TB.java ; This file is part of Twister.
Version: 2.005

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

import java.util.List;
import java.util.ArrayList;
import java.awt.datatransfer.UnsupportedFlavorException;
import javax.swing.tree.TreeNode;
import java.awt.datatransfer.Transferable;
import javax.swing.JComponent;
import java.awt.datatransfer.DataFlavor;
import javax.swing.TransferHandler;
import javax.swing.JPanel;
import java.awt.Color;
import java.util.HashMap;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.net.URL;
import java.util.Iterator;
import java.util.Set;
import javax.swing.JTree;
import javax.swing.JScrollPane;
import javax.swing.tree.TreeSelectionModel;
import javax.swing.BorderFactory;
import javax.swing.border.BevelBorder;
import javax.swing.GroupLayout;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.DefaultMutableTreeNode;
import java.awt.event.MouseAdapter;
import java.awt.event.KeyAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import javax.swing.tree.TreePath;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import com.twister.CustomDialog;
import javax.swing.JOptionPane;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JButton;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import java.awt.BorderLayout;
import java.awt.Container;
import javax.swing.AbstractAction;
import com.twister.MySftpBrowser;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;

public class TB extends JPanel{
    private XmlRpcClient client;
    private Node parent;
    private JTree tree;
    private DefaultMutableTreeNode root;
    private NodePanel optpan;
    private JButton add, remove;
    private JScrollPane jScrollPane1;

    public TB(){
        initializeRPC();
        initPanel();
        parent = getTB("/",null);
        buildTree(parent,root);
        ((DefaultTreeModel)tree.getModel()).reload();
    }

    public void initPanel(){
        setBorder(BorderFactory.createTitledBorder("Test Beds"));
        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(null);
        
        add = new JButton("Add TB");
        add.setBounds(0,5,155,20);
        buttonPanel.add(add);
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addComp();
            }
        });
        
        remove = new JButton("Remove");
        remove.setBounds(160,5,100,20);
        remove.setEnabled(false);
        buttonPanel.add(remove);
        remove.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(optpan.tname.getText().equals(""))return;
                removeComp();
            }
        });
        
        root = new DefaultMutableTreeNode("root", true);
        tree = new JTree(root);
        tree.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(ev.getKeyCode()==KeyEvent.VK_C && ev.isControlDown()){
                    try{if(tree.getSelectionPath()==null){return;}
                        String s = tree.getSelectionPath().getLastPathComponent().toString();
                        s = s.replace("ID: ","");
                        s = s.replace("Path: ","");
                        StringSelection selection = new StringSelection(s);
                        Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
                        clipboard.setContents(selection, selection);
                    } catch(Exception e){
                        e.printStackTrace();
                    }
                }
            }});
        tree.setTransferHandler(new TreeTransferHandler());  
        tree.setCellRenderer(new CustomIconRenderer());
        
        optpan = new NodePanel(tree,client);
        tree.setDragEnabled(true);
        tree.setRootVisible(false);
        tree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
        jScrollPane1 = new JScrollPane();
        tree.setBorder(BorderFactory.createBevelBorder(BevelBorder.LOWERED));
        jScrollPane1.setViewportView(tree);
        
        JPanel treepanel = new JPanel();
        treepanel.setLayout(new java.awt.BorderLayout());
        treepanel.add(jScrollPane1, java.awt.BorderLayout.CENTER);
        
        JMenuBar menubar = new JMenuBar();
        JMenu menu = new JMenu("File");
        menubar.add(menu);
        treepanel.add(menubar,BorderLayout.NORTH);
        JMenuItem imp = new JMenuItem("Import from XML");
        imp.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                Container c;
                if(RunnerRepository.container!=null)c = RunnerRepository.container.getParent();
                else c = RunnerRepository.window;
                final JTextField tf = new JTextField();
                new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,tf,c,false).setAction(new AbstractAction(){
                    public void actionPerformed(ActionEvent ev){
                        try{
                            String resp = client.execute("import_xml", new Object[]{tf.getText(),1}).toString();
                            System.out.println(resp);
                            if(resp.equals("true")){
                                root.removeAllChildren();
                                parent = getTB("/",null);
                                DefaultTreeModel model = (DefaultTreeModel)tree.getModel();
                                buildTree(parent,root);
                                ((DefaultTreeModel)tree.getModel()).reload();
                            } else {
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
                            }
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                });
            }});
        menu.add(imp);
        JMenuItem exp = new JMenuItem("Export to XML");
        exp.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                Container c;
                if(RunnerRepository.container!=null)c = RunnerRepository.container.getParent();
                else c = RunnerRepository.window;
                final JTextField tf = new JTextField();
                try{tf.setText(RunnerRepository.getTestConfigPath());
                }catch(Exception e){
                    e.printStackTrace();
                }
                AbstractAction action = new AbstractAction(){
                    public void actionPerformed(ActionEvent ev){
                        try{
                            String resp = client.execute("export_xml", new Object[]{tf.getText(),1}).toString();
                            System.out.println(resp);
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                };
                new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,tf,c,false).setAction(action);
            }});
        menu.add(exp);
        
        
        
        GroupLayout layout = new GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                     .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 351, Short.MAX_VALUE)
                    .addComponent(buttonPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(treepanel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addComponent(optpan, GroupLayout.PREFERRED_SIZE, 450, GroupLayout.PREFERRED_SIZE)
                )
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.TRAILING)
                    .addComponent(optpan, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addGroup(layout.createSequentialGroup()
//                         .addComponent(jScrollPane1)
                        .addComponent(treepanel, javax.swing.GroupLayout.DEFAULT_SIZE, 454, Short.MAX_VALUE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(buttonPanel, GroupLayout.PREFERRED_SIZE, 47, GroupLayout.PREFERRED_SIZE)))
                )
        );       
        
        tree.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(ev.getKeyCode()==KeyEvent.VK_DELETE){
                    TreePath tp = tree.getSelectionPath();
                    if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Node){
                        DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                        Node node = (Node)treenode.getUserObject();
                        removeNode(node,treenode);
                        add.setText("Add TB");
                        remove.setEnabled(false);
                    }
                }
            }
        });
        tree.addMouseListener(new MouseAdapter(){
            public void mouseReleased(MouseEvent ev){
                TreePath tp = tree.getPathForLocation(ev.getX(), ev.getY());
                if (tp != null){
                    tree.setSelectionPath(tp);
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Node){
                            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            Node node = (Node)treenode.getUserObject();
                            showNodePopUp(treenode,ev,node);
                            add.setText("Add Component");
                            remove.setEnabled(true);
                        }
                    } else{
                        if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Node){
                            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            Node node = (Node)treenode.getUserObject();
                            optpan.setParent(node,treenode);
                            add.setText("Add Component");
                            remove.setEnabled(true);
                            add.setEnabled(true);
                        } else {
                            optpan.setParent(null,null);
                            add.setEnabled(false);
                            remove.setEnabled(false);
                        }
                    }
                } else {
                    add.setText("Add TB");
                    remove.setEnabled(false);
                    tree.setSelectionPath(null);
                    optpan.setParent(null,null);
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        addRootNodePopUp(ev);
                    } 
                }}});
    }
    
    public JTree getTree(){
        return tree;
    }   
    
    public void removeComp(){
        
        TreePath tp = tree.getSelectionPath();
        DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
        Node node = (Node)treenode.getUserObject();
        removeNode(node,treenode);
    }
    
    public void addComp(){
        if(add.getText().equals("Add TB")){
            addTestBed();
        } else {
            TreePath tp = tree.getSelectionPath();
            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
            Node node = (Node)treenode.getUserObject();
            appendNode(treenode,node);
        }
    }
    
    public void setTree(JTree tree){
        jScrollPane1.setViewportView(tree);
    }
    
    public void addRootNodePopUp(MouseEvent ev){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Add TestBed");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addTestBed();
            }});
        p.add(item);
        p.show(this.tree,ev.getX(),ev.getY());
    }
    
    public void addTestBed(){
        String resp = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, 
                                                    TB.this, "Name", "TestBed name: ");
        if(resp!=null&&!resp.equals("")){
            boolean goon=true;
            for(String s:parent.getChildren().keySet()){
                if(resp.equals(parent.getChildren().get(s).getName())){
                    goon = false;
                    break;
                }
            }
            if(goon){
                try{
                    Node newnode = new Node(null,resp,resp,parent,null,(byte)0);
                    resp = client.execute("setResource", new Object[]{resp,"/",null}).toString();
                    if(resp.indexOf("ERROR")==-1){
                        parent.addChild(resp, newnode);
                        newnode.setID(resp);
                        DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(newnode);
                        DefaultMutableTreeNode root = (DefaultMutableTreeNode)((DefaultTreeModel)tree.getModel()).getRoot();
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, root,root.getChildCount());
                        
                        DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+newnode.getID());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treechild,treechild.getChildCount());
                        
                        DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(newnode.getPath());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treechild,treechild.getChildCount());
                        
                        if(root.getChildCount()==1){
                            ((DefaultTreeModel)tree.getModel()).reload();
                        }
                    } else {
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,RunnerRepository.window,"Warning", resp);
                    }
                } catch (Exception e){
                    e.printStackTrace();
                }
            } else {
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,RunnerRepository.window,"Warning", 
                                        "There is a TB with the same name, please use different name.");
            }
        }    
    }
    
    /*
     * popup user on Node
     * right click
     */
    public void showNodePopUp(final DefaultMutableTreeNode treenode,MouseEvent ev,final Node node){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Add Component");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                appendNode(treenode,node);}});
        p.add(item);
        item = new JMenuItem("Remove");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                removeNode(node,treenode);}});
        p.add(item);
        p.show(this.tree,ev.getX(),ev.getY());
    }
    
    /*
     * create and append new node 
     * to this parent node
     */
    public void appendNode(DefaultMutableTreeNode treenode, Node parent){
        String resp = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, 
                                                    this, "Name", "Component name: ");
        if(resp!=null&&!resp.equals("")){
            boolean goon=true;
            for(String s:parent.getChildren().keySet()){
                if(resp.equals(parent.getChildren().get(s).getName())){
                    goon = false;
                    break;
                }
            }
            if(goon){
                try{
                    Node newnode = new Node(null,parent.getPath().getPath()+"/"+resp,resp,parent,null,(byte)(1));
                    resp = client.execute("setResource", new Object[]{resp,parent.getID(),null}).toString();
                    if(resp.indexOf("ERROR")==-1){
                        parent.addChild(resp,newnode);
                        
                        newnode.setID(resp);
                        DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(newnode);
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, treenode,treenode.getChildCount());
                        
                        DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+newnode.getID());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treechild,treechild.getChildCount());
                        
                        DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(newnode.getPath());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treechild,treechild.getChildCount());
                    } else {
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,RunnerRepository.window,"Warning", resp);
                    }                
                } catch (Exception e){
                    e.printStackTrace();
                }
            } else {
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,RunnerRepository.window,"Warning", 
                                    "There is a component with the same name, please use another name.");
            }
        }
    }
    
    /*
     * remove node
     */
    public boolean removeNode(Node node,DefaultMutableTreeNode treenode){
        try{String s = client.execute("deleteResource", new Object[]{node.getID()}).toString();
            if(s.equals("true")){
                Node parent = node.getParent();
                if(parent!=null){
                    parent.removeChild(node.getID());
                }
                ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(treenode);
                optpan.setParent(null,null);
                remove.setEnabled(false);
                add.setText("Add TB");
                return true;
            }
            return false;
        }
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
    
    /*
     * print tree nodes name
     * starting from node
     */
    public void printTree(Node node){
        System.out.println("Name: "+node.getName());
        Iterator iter = node.getChildren().keySet().iterator();
        while(iter.hasNext()){
            String childid = iter.next().toString();
            printTree(node.getChild(childid));
        }
    }
    
    
    /*
     * build whole 
     * structure from scratch
     */
    public void buildTree(Node node, DefaultMutableTreeNode treenode){
        try{
            Iterator iter = node.getChildren().keySet().iterator();
            while(iter.hasNext()){
                String childid = iter.next().toString();
                Node child = getTB(childid,node);
                node.addChild(childid, child);
                DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(child);
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, treenode,treenode.getChildCount());
                DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+child.getID());
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treechild,treechild.getChildCount());
                DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(child.getPath());
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treechild,treechild.getChildCount());
                buildTree(child,treechild);
            }
        } catch(Exception e){
            e.printStackTrace();
        }
    }

    /*
     * create a node based om an id
     * the node is created from the data 
     * received from server
     */
    public Node getTB(String id,Node parent){
        try{HashMap hash= (HashMap)client.execute("getResource", new Object[]{id});
            String path = hash.get("path").toString();
            String name = path.split("/")[path.split("/").length-1];
            byte type = 1;
            if(parent!=null&&parent.toString().equals("")){
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
                    if(n.equals("epnames")){
                        node.setEPs(meta.get(n).toString());
                        continue;
                    }
                    node.addProperty(n, meta.get(n).toString());
                }
            }
            return node;
        }catch(Exception e){
            System.out.println("requested id: "+id);
            try{System.out.println("server respons: "+client.execute("getResource", new Object[]{id}));}
            catch(Exception ex){ex.printStackTrace();}
            e.printStackTrace();
            return null;
        }
    }
    
    
    //get the parent Node
    public Node getParentNode(){
        return parent;
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
            System.out.println("XMLRPC Client for testbed initialized: "+client);}
        catch(Exception e){System.out.println("Could not conect to "+
                            RunnerRepository.host+" :"+RunnerRepository.getCentralEnginePort()+"/ra/"+
                            "for RPC client initialization");}
    }
}


class TreeTransferHandler extends TransferHandler {  
    
    
    DataFlavor nodesFlavor;  
    DataFlavor[] flavors = new DataFlavor[1];
   
    public TreeTransferHandler() {  
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
   
//     public boolean canImport(TransferHandler.TransferSupport support) {  
//         if(!support.isDrop()) {  
//             return false;  
//         }  
//         support.setShowDropLocation(true);  
//         if(!support.isDataFlavorSupported(nodesFlavor)) {  
//             return false;  
//         }  
//         // Do not allow a drop on the drag source selections.  
//         JTree.DropLocation dl =  
//                 (JTree.DropLocation)support.getDropLocation();  
//         JTree tree = (JTree)support.getComponent();  
//         int dropRow = tree.getRowForPath(dl.getPath());  
//         int[] selRows = tree.getSelectionRows();  
//         for(int i = 0; i < selRows.length; i++) {  
//             if(selRows[i] == dropRow) {  
//                 return false;  
//             }  
//         }  
//         // Do not allow MOVE-action drops if a non-leaf node is  
//         // selected unless all of its children are also selected.  
// //             int action = support.getDropAction();  
// //             if(action == MOVE) {  
// //                 return haveCompleteNode(tree);  
// //             }  
//         // Do not allow a non-leaf node to be copied to a level  
//         // which is less than its source level.  
//         TreePath dest = dl.getPath();  
//         DefaultMutableTreeNode target =  
//             (DefaultMutableTreeNode)dest.getLastPathComponent();  
//         TreePath path = tree.getPathForRow(selRows[0]);  
//         DefaultMutableTreeNode firstNode =  
//             (DefaultMutableTreeNode)path.getLastPathComponent();  
//         if(firstNode.getChildCount() > 0 &&  
//                target.getLevel() < firstNode.getLevel()) {  
//             return false;  
//         }  
//         return true;  
//     }  
   
//     private boolean haveCompleteNode(JTree tree) {  
//         int[] selRows = tree.getSelectionRows();  
//         TreePath path = tree.getPathForRow(selRows[0]);  
//         DefaultMutableTreeNode first =  
//             (DefaultMutableTreeNode)path.getLastPathComponent();  
//         int childCount = first.getChildCount();  
//         // first has children and no children are selected.  
//         if(childCount > 0 && selRows.length == 1)  
//             return false;  
//         // first may have children.  
//         for(int i = 1; i < selRows.length; i++) {  
//             path = tree.getPathForRow(selRows[i]);  
//             DefaultMutableTreeNode next =  
//                 (DefaultMutableTreeNode)path.getLastPathComponent();  
//             if(first.isNodeChild(next)) {  
//                 // Found a child of first.  
//                 if(childCount > selRows.length-1) {  
//                     // Not all children of first are selected.  
//                     return false;  
//                 }  
//             }  
//         }  
//         return true;  
//     }  
   
    protected Transferable createTransferable(JComponent c) {  
        JTree tree = (JTree)c;  
        TreePath[] paths = tree.getSelectionPaths();  
        if(paths != null) {  
            // Make up a node array of copies for transfer and  
            // another for/of the nodes that will be removed in  
            // exportDone after a successful drop.  
            List<Node> copies =  new ArrayList<Node>();  
//             List<DefaultMutableTreeNode> toRemove =  
//                 new ArrayList<DefaultMutableTreeNode>();  
            DefaultMutableTreeNode node =  (DefaultMutableTreeNode)paths[0].getLastPathComponent();  
            Node copy = copy((Node)node.getUserObject());
            copies.add(copy);  
//             toRemove.add(node);  
            for(int i = 1; i < paths.length; i++) {  
                DefaultMutableTreeNode next =  
                    (DefaultMutableTreeNode)paths[i].getLastPathComponent();  
                // Do not allow higher level nodes to be added to list.  
                if(next.getLevel() < node.getLevel()) {  
                    break;  
                } else if(next.getLevel() > node.getLevel()) {  // child node  
//                     copy.add(copy((Node)next.getUserObject()));  
                    // node already contains child  
                } else {                                        // sibling  
                    copies.add(copy((Node)next.getUserObject()));  
//                     toRemove.add(next);  
                }  
            }  
            Node[] nodes =  
                copies.toArray(new Node[copies.size()]);
            return new NodesTransferable(nodes);  
        }  
        return null;  
    }  
   
    /** Defensive copy used in createTransferable. */  
    private Node copy(Node node) {  
        return node.clone();  
    }  
   
//     protected void exportDone(JComponent source, Transferable data, int action) {  
//         if((action & MOVE) == MOVE) {  
//             JTree tree = (JTree)source;  
//             DefaultTreeModel model = (DefaultTreeModel)tree.getModel();  
//             // Remove nodes saved in nodesToRemove in createTransferable.  
//             for(int i = 0; i < nodesToRemove.length; i++) {  
//                 model.removeNodeFromParent(nodesToRemove[i]);  
//             }  
//         }  
//     }  
   
    public int getSourceActions(JComponent c) {  
        return MOVE;  
    }  
   
//     public boolean importData(TransferHandler.TransferSupport support) {  
//         if(!canImport(support)) {  
//             return false;  
//         }  
//         // Extract transfer data.  
//         DefaultMutableTreeNode[] nodes = null;  
//         try {  
//             Transferable t = support.getTransferable();  
//             nodes = (DefaultMutableTreeNode[])t.getTransferData(nodesFlavor);  
//         } catch(UnsupportedFlavorException ufe) {  
//             System.out.println("UnsupportedFlavor: " + ufe.getMessage());  
//         } catch(java.io.IOException ioe) {  
//             System.out.println("I/O error: " + ioe.getMessage());  
//         }  
//         // Get drop location info.  
//         JTree.DropLocation dl =  
//                 (JTree.DropLocation)support.getDropLocation();  
//         int childIndex = dl.getChildIndex();  
//         TreePath dest = dl.getPath();  
//         DefaultMutableTreeNode parent =  
//             (DefaultMutableTreeNode)dest.getLastPathComponent();  
//         JTree tree = (JTree)support.getComponent();  
//         DefaultTreeModel model = (DefaultTreeModel)tree.getModel();  
//         // Configure for drop mode.  
//         int index = childIndex;    // DropMode.INSERT  
//         if(childIndex == -1) {     // DropMode.ON  
//             index = parent.getChildCount();  
//         }  
//         // Add data to model.  
//         for(int i = 0; i < nodes.length; i++) {  
//             model.insertNodeInto(nodes[i], parent, index++);  
//         }  
//         return true;  
//     }  
   
    public String toString() {  
        return getClass().getName();  
    }  
   
    public class NodesTransferable implements Transferable {  
        Node[] nodes;  
   
        public NodesTransferable(Node[] nodes) {  
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
