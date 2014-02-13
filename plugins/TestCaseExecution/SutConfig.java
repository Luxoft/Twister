/*
File: SutConfig.java ; This file is part of Twister.
Version: 2.004

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
import javax.swing.JTree;
import java.awt.BorderLayout;
import javax.swing.tree.DefaultMutableTreeNode;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.awt.datatransfer.UnsupportedFlavorException;
import javax.swing.tree.TreeNode;
import java.awt.datatransfer.Transferable;
import javax.swing.JComponent;
import java.awt.datatransfer.DataFlavor;
import javax.swing.TransferHandler;
import javax.swing.tree.TreeSelectionModel;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.JScrollPane;
import java.util.HashMap;
import java.net.URL;
import java.util.Set;
import java.util.Iterator;
import javax.swing.tree.TreePath;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.JFrame;
import javax.swing.JProgressBar;

public class SutConfig extends JPanel{
    public JTree tree;
    public DefaultMutableTreeNode root;
    public XmlRpcClient client;
    private JFrame progress;
    
    public SutConfig(){
        setLayout(new BorderLayout());
        tree = new JTree();
        tree.addMouseListener(new MouseAdapter(){
            public void mouseReleased(final MouseEvent ev){
                if(ev.getClickCount()==2){
                    TreePath tp = tree.getPathForLocation(ev.getX(), ev.getY());
                    final DefaultMutableTreeNode tn = (DefaultMutableTreeNode)tp.getLastPathComponent();
//                     if(!tree.isExpanded(new TreePath(tn.getPath())))return;
                    if(!tree.isExpanded(tp))return;
                    if(tn.getLevel()==1){
                        new Thread(){
                            public void run(){
                                startProgressBar(ev.getXOnScreen(),ev.getYOnScreen());
                                tn.removeAllChildren();
                                ((DefaultTreeModel)tree.getModel()).reload(tn);
                                SUT s = (SUT)tn.getUserObject();
                                String eps = "";
                                try{
                                    String lock = client.execute("isSutLocked", new Object[]{s.getID()}).toString();
                                    if(!lock.equals("false")&&lock.indexOf("*ERROR*")==-1){
                                        s.setLock(lock);
                                    }else{
                                        s.setLock("");
                                    }
                                    String resp = client.execute("isSutReserved", new Object[]{s.getID()}).toString();
                                    if(!resp.equals("false")&&resp.indexOf("*ERROR*")==-1){
                                        s.setReserved(resp);
                                    } else {
                                        s.setReserved("");
                                    }
                                } catch (Exception e){
                                    System.out.println("Could not get status for: "+s.getName());
                                    e.printStackTrace();
                                }
                                
                                try{HashMap hash= (HashMap)client.execute("getSut", new Object[]{s.getID(),RunnerRepository.user,RunnerRepository.user});
                                    try{eps = ((HashMap)hash.get("meta")).get("_epnames_"+RunnerRepository.user).toString();}
                                    catch(Exception e){
                                        eps = "";
                                    }
                                    DefaultMutableTreeNode epsnode = new DefaultMutableTreeNode("EP: "+eps,false);
                                    s.setEPNode(epsnode);
                                    ((DefaultTreeModel)tree.getModel()).insertNodeInto(epsnode, tn, tn.getChildCount());
                                    Object[] children = (Object[])hash.get("children");
                                    buildChildren(children,tn);
                                }catch(Exception e){
                                    System.out.println("Could not get resources for: "+tn.toString());
                                    e.printStackTrace();
                                }
                                progress.dispose();
                         }
                    }.start();
                    }
                }
            }
        });
        tree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
        root = new DefaultMutableTreeNode("root");
        DefaultTreeModel treemodel = new DefaultTreeModel(root,true);
        tree.setModel(treemodel);
        tree.setRootVisible(false);
        tree.setCellRenderer(new CustomIconRenderer());
        JScrollPane sp = new JScrollPane(tree);
        add(sp,BorderLayout.CENTER);
        tree.setTransferHandler(new ImportTreeTransferHandler());
        tree.setDragEnabled(true);
        initializeRPC();
    }
    
    public void startProgressBar(final int X, final int Y){            
        progress = new JFrame();
        progress.setAlwaysOnTop(true);
        progress.setLocation(X,Y);
        progress.setUndecorated(true);
        JProgressBar bar = new JProgressBar();
        bar.setIndeterminate(true);
        progress.add(bar);
        progress.pack();
        progress.setVisible(true);
    }
    
//     public void getSUT(){
//         try{HashMap hash= (HashMap)client.execute("getSut", new Object[]{"/",RunnerRepository.user,RunnerRepository.user});
//             Object[] children = (Object[])hash.get("children");
//             DefaultMutableTreeNode child,epsnode;
//             DefaultTreeModel model = (DefaultTreeModel)tree.getModel();
//             root.removeAllChildren();
//             String name,path,eps,id;
//             Object[] subchildren;
//             for(Object o:children){
//                 hash= (HashMap)client.execute("getSut", new Object[]{o.toString(),RunnerRepository.user,RunnerRepository.user});
//                 path = hash.get("path").toString();
//                 id = hash.get("id").toString();
//                 name = path.split("/")[path.split("/").length-1];
//                 try{eps = ((HashMap)hash.get("meta")).get("_epnames_"+RunnerRepository.user).toString();}
//                 catch(Exception e){eps = "";}
//                 name = name.replace(".system", "(system)");
//                 name = name.replace(".user", "(user)");                
//                 SUT s = new SUT(name,eps);
//                 s.setID(id);
//                 epsnode = new DefaultMutableTreeNode("EP: "+eps,false);
//                 s.setEPNode(epsnode);
//                 child = new DefaultMutableTreeNode(s);
//                 child.add(epsnode);                
//                 subchildren = (Object[])hash.get("children");
//                 for(Object ob:subchildren){
//                     String childid = ob.toString();
//                     HashMap subhash= (HashMap)client.execute("getSut", new Object[]{childid,RunnerRepository.user,RunnerRepository.user});
//                     id = subhash.get("id").toString();
//                     buildChildren(new Object[]{id},child);
//                 }
//                 model.insertNodeInto(child, root, root.getChildCount());
//             }
//         } catch (Exception e){
//             e.printStackTrace();
//         }
//     }
    
    private void buildChildren(Object [] children, DefaultMutableTreeNode treenode){
        String childid, subchildid;
        for(Object o:children){
            try{childid = o.toString();
                System.out.println(childid+" - "+treenode.toString());
                HashMap subhash= (HashMap)client.execute("getSut", new Object[]{childid,RunnerRepository.user,RunnerRepository.user});
                String subpath = subhash.get("path").toString();
                String subname = subpath.split("/")[subpath.split("/").length-1];
                HashMap meta = (HashMap)subhash.get("meta");
                String id = subhash.get("id").toString();
                Comp comp = new Comp(subname,id,meta.get("_id")+"");
                DefaultMutableTreeNode component = new DefaultMutableTreeNode(comp,true);
                DefaultMutableTreeNode nodeid = new DefaultMutableTreeNode("ID: "+id,false);
                component.add(nodeid);
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(component, treenode, treenode.getChildCount());
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
    
    public void initializeRPC(){
        try{XmlRpcClientConfigImpl configuration = new XmlRpcClientConfigImpl();
            configuration.setServerURL(new URL("http://"+RunnerRepository.host+
                                        ":"+RunnerRepository.getCentralEnginePort()+"/ra/"));
            configuration.setEnabledForExtensions(true);
            configuration.setBasicPassword(RunnerRepository.password);
            configuration.setBasicUserName(RunnerRepository.user);
            client = new XmlRpcClient();
            client.setConfig(configuration);
            System.out.println("XMLRPC Client for SutConfig initialized: "+client);}
        catch(Exception e){System.out.println("Could not conect to "+
                            RunnerRepository.host+" :"+RunnerRepository.getCentralEnginePort()+"/ra/"+
                            "for RPC client initialization");}
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
            System.out.println("requested id: "+id);
            try{System.out.println("server respons: "+client.execute("getResource", new Object[]{id}));}
            catch(Exception ex){ex.printStackTrace();}
            e.printStackTrace();
            return null;
        }
    }
    
    public void getFirstLevel(){
        root.removeAllChildren();
        ((DefaultTreeModel)tree.getModel()).reload();
        String sutfiles [][] = RunnerRepository.window.mainpanel.p4.getSut().sut.getSutTree().getSutFiles();
        int size = sutfiles.length;
        String sut;
        for(int i=0;i<size;i++){
            sut = sutfiles[i][0];
//         }
//         for(String sut:sutfiles){
            SUT s = new SUT(sut,null);
            sut = sut.replace("(system)", ".system");
            sut = sut.replace("(user)", ".user");
            if(!sutfiles[i][1].equals("free")){
                if(sutfiles[i][1].equals("locked")){
                    s.setLock(sutfiles[i][2]);
                }else{
                    s.setReserved(sutfiles[i][2]);
                }
            }
            s.setID("/"+sut);
            DefaultMutableTreeNode child = new DefaultMutableTreeNode(s);
            ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, root, root.getChildCount());
        }
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
            return false;
        }
        
        protected Transferable createTransferable(JComponent c) {
            JTree tree = (JTree)c;  
            TreePath path = tree.getSelectionPath();
            if(path != null) {
                StringBuilder sb = new StringBuilder();
                Object [] paths = path.getPath();
                paths[1] = paths[1].toString().replace(".system","(system)");
                paths[1] = paths[1].toString().replace(".user","(user)");
                sb.append(paths[1]);
                for(int i=2;i<paths.length;i++){
                    sb.append("/");
                    sb.append(paths[i]);
                }
                DefaultMutableTreeNode node =  (DefaultMutableTreeNode)path.getLastPathComponent();
                if(node.getUserObject() instanceof SUT){   
                    System.out.println(((SUT)node.getUserObject()).getID()+" - "+sb.toString());
                    return new StringTransferable(((SUT)node.getUserObject()).getID()+" - "+sb.toString());
                } else if(node.getUserObject() instanceof Comp){
                    System.out.println(((Comp)node.getUserObject()).getID()+" - "+sb.toString());
                    return new StringTransferable(((Comp)node.getUserObject()).getID()+" - "+sb.toString());
                } else return null;
            }
            return null;  
        }
         
        private DefaultMutableTreeNode copy(TreeNode node) {  
            return new DefaultMutableTreeNode(node);  
        } 
        
        public int getSourceActions(JComponent c) {  
            return COPY;  
        }  
       
        public boolean importData(TransferHandler.TransferSupport support) {  
            return false;
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
       
        public class StringTransferable implements Transferable {  
            String file;  
            DataFlavor nodesFlavor;  
            DataFlavor[] flavors = new DataFlavor[1];
       
            public StringTransferable(String file) {  
                this.file = file;  
                try {  
                    String mimeType = DataFlavor.javaJVMLocalObjectMimeType +  
                                      ";class=\"" +  
                                      String.class.getName() +  
                                      "\"";  
                    nodesFlavor = new DataFlavor(mimeType);  
                    flavors[0] = nodesFlavor;  
                } catch(ClassNotFoundException e) {  
                    System.out.println("ClassNotFound: " + e.getMessage());  
                }  
             }  
       
            public Object getTransferData(DataFlavor flavor)  
                                     throws UnsupportedFlavorException {  
                if(!isDataFlavorSupported(flavor))  
                    throw new UnsupportedFlavorException(flavor);  
                return file;  
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