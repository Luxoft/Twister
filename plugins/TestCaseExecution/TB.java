/*
File: TB.java ; This file is part of Twister.
Version: 2.013

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
import java.awt.event.HierarchyListener;
import java.awt.event.HierarchyEvent;
import javax.swing.DropMode;
import java.util.Enumeration;
import javax.swing.JFrame;
import javax.swing.JProgressBar;

public class TB extends JPanel{
    private XmlRpcClient client;
    private Node parent;
    private JTree tree;
    public DefaultMutableTreeNode root;
    private NodePanel optpan;
    private JButton add, remove;
    private JScrollPane jScrollPane1;
    private JLabel jusers;
    private JFrame progress;

    public TB(){
        initializeRPC();
        initPanel();
        parent = getTB("/",null);
        //refreshTBs();
        ((DefaultTreeModel)tree.getModel()).reload();
    }

    public void initPanel(){
        setBorder(BorderFactory.createTitledBorder("Test Beds"));
        final JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(null);
        
        add = new JButton("Add TB");
        add.setBounds(0,5,155,20);
        if(PermissionValidator.canEditTB())buttonPanel.add(add);
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addComp();
            }
        });
        
        remove = new JButton("Remove");
        remove.setBounds(160,5,100,20);
        remove.setEnabled(false);
        if(PermissionValidator.canEditTB())buttonPanel.add(remove);
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
        tree.addMouseListener(new MouseAdapter(){
            public void mouseReleased(final MouseEvent ev){
                if(ev.getClickCount()==2){
                    TreePath tp = tree.getPathForLocation(ev.getX(), ev.getY());
                    final DefaultMutableTreeNode tn = (DefaultMutableTreeNode)tp.getLastPathComponent();
                    if(tn.getChildCount()>0&&!tree.isExpanded(new TreePath(tn.getPath())))return;
                    if(((Node)tn.getUserObject()).getReserved().equals(RunnerRepository.user))return;
                    if(tn.getLevel()==1){
                     new Thread(){
                            public void run(){    
                                startProgressBar(ev.getXOnScreen(),ev.getYOnScreen());
                                DefaultTreeModel model = ((DefaultTreeModel)tree.getModel());
                                tn.removeAllChildren();
                                model.reload(tn);
                                Node node = getTB("/"+((Node)tn.getUserObject()).getName(),null);
                                tn.setUserObject(node);
                                DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+node.getID());
                                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, tn,0);
                                DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(node.getPath());
                                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, tn,1);
                                buildTree(node,tn,false);
                                model.reload(tn);
                                tree.expandPath(new TreePath(tn.getPath()));
                                progress.dispose();
                            }
                        }.start();
                    }
                }
            }
        });
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
        JPanel upperpanel = new JPanel();
        upperpanel.setLayout(new java.awt.BorderLayout());
        JPanel activetbusers = new JPanel();
        activetbusers.setLayout(new BorderLayout());
        jusers = new JLabel("TB Active Users:");
        jusers.setBorder(BorderFactory.createEmptyBorder(0, 5, 0, 0));
        JButton refreshtb = new JButton("Refresh TBs");
        activetbusers.add(refreshtb,BorderLayout.WEST);
        refreshtb.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                buildFirstLevelTB();
            }});
        JMenuBar menubar = new JMenuBar();
        JMenu menu = new JMenu("File");
        menubar.add(menu);
        treepanel.add(upperpanel,BorderLayout.NORTH);
        upperpanel.add(activetbusers,BorderLayout.NORTH);
        upperpanel.add(menubar,BorderLayout.CENTER);

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
                            if(resp.indexOf("*ERROR*")==-1){
                                root.removeAllChildren();
                                parent = getTB("/",null);
                                DefaultTreeModel model = (DefaultTreeModel)tree.getModel();
                                buildTree(parent,root,true);
                                ((DefaultTreeModel)tree.getModel()).reload();
                            } else {
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", "Could not import!CE error: "+resp);
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
                            if(resp.indexOf("*ERROR*")!=-1){
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", "Could not save");
                            }
                            System.out.println(resp);
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                };
                MySftpBrowser browser = new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,tf,c,false);
                browser.setAction(action);
                browser.setButtonText("Save");
            }});
        menu.add(exp);
        GroupLayout layout = new GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(buttonPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(treepanel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addComponent(optpan, GroupLayout.PREFERRED_SIZE, 450, GroupLayout.PREFERRED_SIZE)));
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.TRAILING)
                    .addComponent(optpan, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(treepanel, javax.swing.GroupLayout.DEFAULT_SIZE, 454, Short.MAX_VALUE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(buttonPanel, GroupLayout.PREFERRED_SIZE, 47, GroupLayout.PREFERRED_SIZE)))
                )
        );
        tree.addMouseListener(new MouseAdapter(){
            public void mouseReleased(MouseEvent ev){
                TreePath tp = tree.getPathForLocation(ev.getX(), ev.getY());
                if (tp != null){
                    tree.setSelectionPath(tp);
                    DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)tp.getLastPathComponent();
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        if(treenode.getUserObject() instanceof Node){
                            Node node = (Node)treenode.getUserObject();
                            if(node.getType()==0){
                                if(node.getReserved().equals(RunnerRepository.user)){
                                    optpan.setParent(node,treenode,true);
                                    add.setText("Add Component");
                                    remove.setEnabled(true);
                                    add.setEnabled(true);
                                } else {
                                    optpan.setParent(node,treenode,false);
                                    if(node.getReserved().equals("")&&node.getLock().equals("")){
                                        remove.setEnabled(true);
                                    }
                                    else{
                                        remove.setEnabled(false);
                                    }
                                   if(!node.getReserved().equals(""))add.setEnabled(false);
                                }
                                showTBPopUp(treenode,node,ev);
                            } else {
                                Object ob = ((DefaultMutableTreeNode)((DefaultTreeModel)tree.getModel()).getPathToRoot(treenode)[1]).getUserObject();
                                if(ob instanceof Node){
                                    String reserved = ((Node)ob).getReserved();
                                    if(reserved.equals(RunnerRepository.user)){
                                        showNodePopUp(treenode,ev,node);
                                        optpan.setParent(node,treenode,true);
                                        add.setText("Add Component");
                                        remove.setEnabled(true);
                                        add.setEnabled(true);
                                    }else {
                                        optpan.setParent(node,treenode,false);
                                        remove.setEnabled(false);
                                        add.setEnabled(false);
                                    }
                                }
                            }
                        }
                        else{
                            optpan.setParent(null,null,false);
                            remove.setEnabled(false);
                            add.setEnabled(false);
                        }
                    } else{
                        if(treenode.getUserObject() instanceof Node){
                            Node node = (Node)treenode.getUserObject();
                            if(node.getType()==0){
                                if(node.getReserved().equals(RunnerRepository.user)){
                                    optpan.setParent(node,treenode,true);
                                    add.setText("Add Component");
                                    remove.setEnabled(true);
                                    add.setEnabled(true);
                                } else {
                                    optpan.setParent(node,treenode,false);
                                    if(node.getReserved().equals("")&&node.getLock().equals(""))remove.setEnabled(true);
                                    else remove.setEnabled(false);
                                    if(!node.getReserved().equals(""))add.setEnabled(false);
                                }
                            } else {
                                Object ob = ((DefaultMutableTreeNode)((DefaultTreeModel)tree.getModel()).getPathToRoot(treenode)[1]).getUserObject();
                                if(ob instanceof Node){
                                    String reserved = ((Node)ob).getReserved();
                                    if(reserved.equals(RunnerRepository.user)){
                                        optpan.setParent(node,treenode,true);
                                        add.setText("Add Component");
                                        remove.setEnabled(true);
                                        add.setEnabled(true);
                                    } else {
                                        optpan.setParent(node,treenode,false);
                                        remove.setEnabled(false);
                                        add.setEnabled(false);
                                    }
                                }
                            }
                        } else {
                            optpan.setParent(null,null,false);
                            add.setEnabled(false);
                            remove.setEnabled(false);
                        }
                    }
                } else {
                    add.setText("Add TB");
                    remove.setEnabled(false);
                    add.setEnabled(true);
                    tree.setSelectionPath(null);
                    optpan.setParent(null,null,false);
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        addRootNodePopUp(ev);
                    }}}});}
                    
    /*
     * release all reserved TB's
     */             
    public void releaseAllResources(){
        Enumeration en = root.children();
        Node node;
        while(en.hasMoreElements()){
            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)en.nextElement();
            node = (Node)(treenode).getUserObject();
            if(isReservedByUser(node.getID())){
                release(node.getID());
                setSavedState(treenode,true);
            }
        }
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
    
    public void buildFirstLevelTB(){
        try{root.removeAllChildren();
            Object ob = client.execute("listAllResources", new Object[]{});
            if(ob.toString().indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", ob.toString());
            }
            Object [] array = (Object[])ob;
            DefaultMutableTreeNode child;
            root.removeAllChildren();
            DefaultTreeModel model = (DefaultTreeModel)tree.getModel();
            String name;
            HashMap hash;
            for(Object object:array){
                hash = (HashMap)object;
                name = hash.get("name").toString();
                Node node = new Node(null,"/"+name,name,null,null,(byte)0);
                String status = hash.get("status").toString();
                String user = "";
                if(!status.equals("free")){
                    user = hash.get("user").toString();
                    if(status.equals("reserved")){
                        node.setReserved(user);
                    }else if(status.equals("locked")){
                        node.setLock(user);
                    }
                }
                child = new DefaultMutableTreeNode(node);
                model.insertNodeInto(child, root, root.getChildCount());
                if(status.equals("reserved")&&user.equals(RunnerRepository.user)){
                    node = getTB("/"+name,null);
                    DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+node.getID());
                    ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, child,0);
                    DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(node.getPath());
                    ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, child,1);
                    ((DefaultTreeModel)tree.getModel()).nodeChanged(child);
                    buildTree(node,child,false);
                }
            }
            model.reload();
            ((DefaultTreeModel)tree.getModel()).reload();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    
    /*
     * refresh tree from server
     */
//     public void refreshTBs(){
        //listAllResources()
//         root.removeAllChildren();
//         parent = getTB("/",null);
//         buildTree(parent,root,true);
//         ((DefaultTreeModel)tree.getModel()).reload();
//         optpan.setParent(null,null,false);
//         remove.setEnabled(false);
//         add.setText("Add TB");
//         Enumeration en = root.children();
//         Node node;
//         while(en.hasMoreElements()){
//             DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)en.nextElement();
//             node = (Node)treenode.getUserObject();
//             node.setReserved(getTBReservdUser(node.getID()));
//             if(node.getReserved().equals(RunnerRepository.user)){
//                 node = getTB(node.getID(),node.getParent());
//                 node.setReserved(RunnerRepository.user);
//                 DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+node.getID());
//                 ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treenode,0);
//                 DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(node.getPath());
//                 ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treenode,1);
//                 ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
//                 buildTree(node,treenode,false);
//                 ((DefaultTreeModel)tree.getModel()).reload(treenode);
//             }
//             try{String resp = client.execute("isResourceLocked", new Object[]{node.getID()}).toString();
//                 if(resp.equals("false")){
//                     node.setLock("");
//                 }
//                 else if (resp.indexOf("*ERROR*")!=-1){
//                     CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
//                     node.setLock("");
//                 } else {
//                     node.setLock(resp);
//                 }
//             } catch (Exception e){e.printStackTrace();}
//             ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
//         }
//     }
    
    /*
     * get from server user that reserved tb
     */
    public String getTBReservdUser(String tbid){
        try{String resp = client.execute("isResourceReserved", new Object[]{tbid,1}).toString();
            if(resp.equals("false")){
                return "";
            }
             else if (resp.indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
                return "";
            }
            else{
                return resp;
            }
        }
        catch(Exception e){e.printStackTrace();
            return "";
        }
    }
    
//     /*
//      * check if a TB is reserved
//      */
//     public boolean isReserved(String tbid){
//         try{String resp = client.execute("isResourceReserved", new Object[]{tbid}).toString();
//             System.out.println(resp);}
//         catch(Exception e){
//             e.printStackTrace();
//             return false;
//         }
//         return true;
//     }
    
    /*
     * check if a TB is reserved
     */
    public boolean isReservedByUser(String tbid){
        try{String resp = client.execute("isResourceReserved", new Object[]{tbid,1}).toString();
            if(resp.equals(RunnerRepository.user)){
                return true;
            } else if (resp.indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
                return false;
            } else {
                return false;
            }
        }
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
    
    /*
     * method used to reserve TB on server
     */
    public boolean reserve(String tbid){
        try{String resp = client.execute("reserveResource", new Object[]{tbid}).toString();
            if(resp.indexOf("*ERROR*")==-1){
                return true;
            } else {
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
                return false;
            }
        }
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
    
    /*
     * method used to release TB on server
     */
    public boolean release(String tbid){
        try{System.out.println("Releasing tb: "+tbid);
            String resp = client.execute("discardAndReleaseReservedResource", new Object[]{tbid,1}).toString();
            if(resp.indexOf("*ERROR*")==-1){
                return true;
            } else {
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
                return false;
            }
        }
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
    
     /*
     * method used to discard and release TB on server
     */
    public boolean discardAndRelease(String tbid){
        try{String resp = client.execute("discardAndReleaseReservedResource", new Object[]{tbid,1}).toString();
            if(resp.indexOf("*ERROR*")==-1){
                return true;
            } else {
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
                return false;
            }
        }
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
    }
    
    /*
     * method to signal server to save
     * latest changes made and release resource
     */
    public boolean saveAndRelease(String tbid){
        try{String resp = client.execute("saveAndReleaseReservedResource", new Object[]{tbid}).toString();
            if(resp.indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
                return false;
            }
            return true;
        }
        catch(Exception e){e.printStackTrace();
            return false;
        }
    }
    
    /*
     * method to signal server to save
     * latest changes made 
     */
    public boolean saveChanges(String tbid){
        try{String resp = client.execute("saveReservedResource", new Object[]{tbid}).toString();
            if(resp.indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
                return false;
            }
            return true;
        }
        catch(Exception e){e.printStackTrace();
            return false;
        }
    }
    
    public void showTBPopUp(final DefaultMutableTreeNode treenode,final Node node,final MouseEvent ev){
        if(!PermissionValidator.canEditTB())return;
        String reserved = node.getReserved();
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Reserve");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent evnt){
                if(reserve("/"+node.getName())){
                    new Thread(){
                        public void run(){
                            DefaultTreeModel model = ((DefaultTreeModel)tree.getModel());
                            startProgressBar(ev.getXOnScreen(),ev.getYOnScreen());
                            treenode.removeAllChildren();
                            model.reload(treenode);
                            Node finalnode = getTB("/"+node.getName(),null);
                            finalnode.setReserved(RunnerRepository.user);
                            DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+finalnode.getID());
                            model.insertNodeInto(temp, treenode,0);
                            DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(finalnode.getPath());
                            model.insertNodeInto(temp2, treenode,1);
                            buildTree(finalnode,treenode,false);
                            treenode.setUserObject(finalnode);
//                             model.nodeChanged(treenode);
                            model.reload(treenode);
                            optpan.setParent(node,treenode,true);
                            remove.setEnabled(true);
                            add.setEnabled(true);
                            add.setText("Add Component");
                            tree.expandPath(new TreePath(treenode.getPath()));
                            progress.dispose();
                        }
                    }.start();
                }
            }});
        p.add(item);
        if(!reserved.equals("")||!node.getLock().equals("")){
            item.setEnabled(false);
        }
        item = new JMenuItem("Release");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                boolean saved = getSavedState(treenode);
                boolean success = false;
                if(saved){
                    success = discardAndRelease("/"+node.getName());
                    node.setReserved("");
                    ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                    optpan.setParent(node,treenode,false);
                } else {
                     int r = (Integer)CustomDialog.showDialog(
                                new JLabel("Save TB before releasing ?"),
                                JOptionPane.QUESTION_MESSAGE, 
                                JOptionPane.OK_CANCEL_OPTION, TB.this, "Save", null);
                    if(r == JOptionPane.OK_OPTION){
                        success = saveAndRelease(node.getID());
                        setSavedState(treenode,true);
                        node.setReserved("");
                        ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                        optpan.setParent(node,treenode,false);
                    } else {
                        success = discardAndRelease(node.getID());
                        buildFirstLevelTB();
                        optpan.setParent(null,null,false);
                    }
                }
                if(success){   
                    //remove.setEnabled(false);
                    add.setText("Add TB");
                }
            }});
        p.add(item);
        if(!reserved.equals(RunnerRepository.user))item.setEnabled(false);
        item = new JMenuItem("Discard Changes & Release");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(discardAndRelease(node.getID())){
                    setSavedState(treenode,true);
                    node.setReserved("");
                    ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                    optpan.setParent(node,treenode,false);
                    //remove.setEnabled(false);
                    add.setText("Add TB");
                }}});
        p.add(item);
        if(!reserved.equals(RunnerRepository.user))item.setEnabled(false);
        if(PermissionValidator.canChangeTBLock()&&reserved.equals("")){
            item = new JMenuItem("Lock");
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    try{String resp = client.execute("lockResource", new Object[]{node.getID()}).toString();
                        if(resp.indexOf("*ERROR*")==-1){
                            node.setLock(RunnerRepository.user);
                            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                            remove.setEnabled(false);
                        } else {
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
                            System.out.println(node.getName()+" was not locked, CE respons: "+resp);
                        }
                    } catch(Exception e){e.printStackTrace();}
                }});
            p.add(item);
            if(!node.getLock().equals(""))item.setEnabled(false);
            item = new JMenuItem("Unlock");
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    try{String resp = client.execute("unlockResource", new Object[]{node.getID()}).toString();
                        if(resp.indexOf("*ERROR*")==-1){
                            node.setLock("");
                            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                            remove.setEnabled(true);
                        } else {
                            System.out.println(node.getName()+" was not unlocked, CE respons: "+resp);                    
                        }
                    } catch (Exception e){
                        e.printStackTrace();
                    }
                }});
            p.add(item);
            if(!node.getLock().equals(RunnerRepository.user))item.setEnabled(false);
        }
        item = new JMenuItem("Save Changes");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(saveChanges(node.getID())){
                    setSavedState(treenode,true);
                }}});
        p.add(item);
        if(!reserved.equals(RunnerRepository.user))item.setEnabled(false);
        p.show(this.tree,ev.getX(),ev.getY());
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
    
    /*
     * sets tree, used for tabs switching
     */
    public void setTree(JTree tree){
        jScrollPane1.setViewportView(tree);
    }
    
    public void addRootNodePopUp(MouseEvent ev){
        if(!PermissionValidator.canEditTB())return;
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
                    if(resp.indexOf("*ERROR*")==-1){                        
                        parent.addChild(resp, newnode);
                        newnode.setID(resp);
                        DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(newnode);
                        DefaultMutableTreeNode root = (DefaultMutableTreeNode)((DefaultTreeModel)tree.getModel()).getRoot();
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, root,root.getChildCount());
                        
                        DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+newnode.getID());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treechild,0);
                        
                        DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(newnode.getPath());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treechild,1);
                        
                        if(root.getChildCount()==1){
                            ((DefaultTreeModel)tree.getModel()).reload();
                        }
                    } else {
                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
                    }
                } catch (Exception e){
                    e.printStackTrace();
                }
            } else {
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,TB.this,"Warning", 
                                        "There is a TB with the same name, please use different name.");
            }
        }    
    }
    
    /*
     * popup user on Node
     * right click
     */
    public void showNodePopUp(final DefaultMutableTreeNode treenode,MouseEvent ev,final Node node){
        if(!PermissionValidator.canEditTB())return;
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
    
    public void setSavedState(DefaultMutableTreeNode treenode,boolean value){
        Node firstparent = (Node)treenode.getUserObjectPath()[1];
        firstparent.setLastSaved(value);
    }
    
    public boolean getSavedState(DefaultMutableTreeNode treenode){
        Node firstparent = (Node)treenode.getUserObjectPath()[1];
        return firstparent.getLastSaved();
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
                    if(resp.indexOf("*ERROR*")==-1){
                        parent.addChild(resp,newnode);
                        setSavedState(treenode,false);
                        newnode.setID(resp);
                        DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(newnode);
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, treenode,treenode.getChildCount());
                        DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+newnode.getID());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treechild,0);
                        
                        DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(newnode.getPath());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treechild,1);
                    } else {
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,TB.this,"Warning", resp);
                    }                
                } catch (Exception e){
                    e.printStackTrace();
                }
            } else {
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,TB.this,"Warning", 
                                    "There is a component with the same name, please use another name.");
            }
        }
    }
    
    /*
     * removes node and updates fields
     */
    public boolean removeNode(Node node,DefaultMutableTreeNode treenode){
        try{String s = client.execute("deleteResource", new Object[]{node.getID()}).toString();
            if(s.indexOf("*ERROR*")==-1){
                Node parent = node.getParent();
                setSavedState(treenode,false);
                if(parent!=null){
                    parent.removeChild(node.getID());
                }
                ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(treenode);
                optpan.setParent(null,null,false);
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
     * build structure from scratch
     */
    public void buildTree(Node node, DefaultMutableTreeNode treenode,boolean onlyfirstlevel){
        try{
            Iterator iter = node.getChildren().keySet().iterator();
            while(iter.hasNext()){
                String childid = iter.next().toString();
                Node child = getTB(childid,node);
                node.addChild(childid, child);
                DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(child);
                ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, treenode,treenode.getChildCount());
                if(!onlyfirstlevel){
                    DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+child.getID());
                    ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treechild,0);
                    DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(child.getPath());
                    ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treechild,1);
                    buildTree(child,treechild,onlyfirstlevel);
                }
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
        try{Object ob = client.execute("getResource", new Object[]{id});
            if(ob.toString().indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", ob.toString());
            }
            HashMap hash = (HashMap)ob;
            String path = hash.get("path").toString();
            String name = path.split("/")[path.split("/").length-1];
            byte type = 1;
            if(parent==null||(parent!=null&&parent.toString().equals(""))){
                type = 0;
            }
            Node node = new Node(hash.get("id").toString(),path,name,parent,null,type);
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
    private void initializeRPC(){
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
            Node[] nodes =  copies.toArray(new Node[copies.size()]);
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
