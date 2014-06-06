/*
File: TB.java ; This file is part of Twister.
Version: 2.027

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
import java.awt.datatransfer.Transferable;
import javax.swing.JComponent;
import java.awt.datatransfer.DataFlavor;
import javax.swing.TransferHandler;
import javax.swing.JPanel;
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
import java.awt.BorderLayout;
import java.awt.Container;
import javax.swing.AbstractAction;
import com.twister.MySftpBrowser;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;
import java.util.Enumeration;
import javax.swing.JFrame;
import javax.swing.JProgressBar;
import java.util.Comparator;
import javax.swing.tree.MutableTreeNode;
import java.util.Arrays;
import java.util.ArrayList;

public class TB extends JPanel{
    private XmlRpcClient client;
    public Node parent;
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
        ((DefaultTreeModel)tree.getModel()).reload();
    }

    public void initPanel(){
        setBorder(BorderFactory.createTitledBorder("Test Beds"));
        final JPanel buttonPanel = new JPanel();
        add = new JButton("Add TB");
        if(PermissionValidator.canEditTB())buttonPanel.add(add);
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                addComp();
            }
        });
        
        remove = new JButton("Remove");
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
                    if(tn.getChildCount()>0&&!tree.isExpanded(tp))return;
                    if(!(tn.getUserObject() instanceof Node))return;
                    if(((Node)tn.getUserObject()).getReserved().equals(RunnerRepository.user))return;
                    if(tn.getLevel()==1){
                        new Thread(){
                            public void run(){    
                                startProgressBar(ev.getXOnScreen(),ev.getYOnScreen());
                                DefaultTreeModel model = ((DefaultTreeModel)tree.getModel());
                                tn.removeAllChildren();
                                model.reload(tn);
                                Node node = getTB("/"+((Node)tn.getUserObject()).getName(),null);
                                node.setReserved(getTBReservdUser("/"+node.getName()));
                                node.setLock(getTBLockedUser("/"+node.getName()));                                
                                tn.setUserObject(node);
                                DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+node.getID());
                                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, tn,0);
                                DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(node.getPath());
                                ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, tn,1);
                                buildTree(node,tn,false);
                                boolean edit = false;
                                if(node.getReserved().equals(RunnerRepository.user)){
                                    edit = true;
                                }
                                optpan.setParent(node,tn,edit);
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
        jusers = new JLabel("TB Active Users:");
        jusers.setBorder(BorderFactory.createEmptyBorder(0, 5, 0, 0));
        JButton refreshtb = new JButton("Refresh TBs");
        activetbusers.add(refreshtb);
        refreshtb.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                Enumeration en = root.children();
                while(en.hasMoreElements()){//check for not saved tb's
                    DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)en.nextElement();
                    if(!((Node)(treenode).getUserObject()).getLastSaved()){
                        String [] buttons = {"Continue","Cancel"};
                        String resp = CustomDialog.showButtons(TB.this, JOptionPane.QUESTION_MESSAGE,
                                                                    JOptionPane.DEFAULT_OPTION, null,buttons ,
                                                                    "Confirmation","All changes will be lost, do you want to continue ?");
                        if (!resp.equals("NULL")) {
                            if(resp.equals("Continue")){
                                ArrayList<String>reserved = new ArrayList();//initial reserved tb's
                                en = root.children();
                                while(en.hasMoreElements()){
                                    treenode = (DefaultMutableTreeNode)en.nextElement();
                                    Node node = (Node)(treenode).getUserObject();
                                    if(isReservedByUser("/"+((Node)(treenode).getUserObject()).getName())){
                                        reserved.add(node.getID());
                                    }
                                }
                                releaseAllResources();//discard all changes and release
                                for(String id:reserved){//reserve the initial reserved tb's
                                    reserve(id);
                                }
                                buildFirstLevelTB();
                            }
                            return;
                        }
                    }
                }
                buildFirstLevelTB();
        }});
        JButton importxml = new JButton("Import XML");
        importxml.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                Container c;
                if(RunnerRepository.container!=null)c = RunnerRepository.container.getParent();
                else c = RunnerRepository.window;
                final JTextField tf = new JTextField(RunnerRepository.REMOTECONFIGDIRECTORY);
                new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,RunnerRepository.CENTRALENGINEPORT,tf,c,false).setAction(new AbstractAction(){
                    public void actionPerformed(ActionEvent ev){
                        try{
                            String resp = client.execute("import_xml", new Object[]{tf.getText()}).toString();
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
        
        JButton exportxml = new JButton("Export XML");
        exportxml.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                Container c;
                if(RunnerRepository.container!=null)c = RunnerRepository.container.getParent();
                else c = RunnerRepository.window;
                final JTextField tf = new JTextField(RunnerRepository.REMOTECONFIGDIRECTORY);
                AbstractAction action = new AbstractAction(){
                    public void actionPerformed(ActionEvent ev){
                        try{
                            String resp = client.execute("export_xml", new Object[]{tf.getText()}).toString();
                            if(resp.indexOf("*ERROR*")!=-1){
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", "Could not save");
                            }
                            System.out.println(resp);
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                };
                MySftpBrowser browser = new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,RunnerRepository.CENTRALENGINEPORT,tf,c,false);
                browser.setAction(action);
                browser.setButtonText("Save");
        }});
            
        activetbusers.add(importxml);
        activetbusers.add(exportxml);
        treepanel.add(upperpanel,BorderLayout.NORTH);
        upperpanel.add(activetbusers,BorderLayout.NORTH);
        GroupLayout layout = new GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(buttonPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(treepanel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addComponent(optpan, GroupLayout.PREFERRED_SIZE, 550, GroupLayout.PREFERRED_SIZE)));
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
                                if(!node.getReserved().equals("")){
                                    remove.setEnabled(false);
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
                                    add.setEnabled(true);
                                } else {
                                    optpan.setParent(node,treenode,false);
                                    if(node.getReserved().equals("")&&node.getLock().equals(""))remove.setEnabled(true);
                                    else remove.setEnabled(false);
                                    if(!node.getReserved().equals(""))add.setEnabled(false);
                                }
                                if(!node.getReserved().equals("")){
                                    remove.setEnabled(false);
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
                    clearParent();
//                     add.setText("Add TB");
//                     remove.setEnabled(false);
//                     add.setEnabled(true);
//                     tree.setSelectionPath(null);
//                     optpan.setParent(null,null,false);
                    if(ev.getButton() == MouseEvent.BUTTON3){
                        addRootNodePopUp(ev);
                    }}}});}
                    
    
    //clear parent and selections
    public void clearParent(){
        add.setText("Add TB");
        remove.setEnabled(false);
        add.setEnabled(true);
        tree.setSelectionPath(null);
        optpan.setParent(null,null,false);
    }
                    
    /*
     * release all reserved TB's
     */             
    public void releaseAllResources(){
        Enumeration en = root.children();
        Node node;
        while(en.hasMoreElements()){
            DefaultMutableTreeNode treenode = (DefaultMutableTreeNode)en.nextElement();
            node = (Node)(treenode).getUserObject();
            if(isReservedByUser("/"+node.getName())){
//                 release("/"+node.getName());
                discardAndRelease("/"+node.getName());
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
            String name,id;
            HashMap hash;
            for(Object object:array){
                hash = (HashMap)object;
                name = hash.get("name").toString();
                id = hash.get("id").toString();
                Node node = new Node(id,"/"+name,name,null,null,(byte)0);
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
                if(status.equals("reserved")&&user.equals(RunnerRepository.user)){
                    node = getTB("/"+name,null);
                    if(!status.equals("free")){
                        user = hash.get("user").toString();
                        if(status.equals("reserved")){
                            node.setReserved(user);
                        }else if(status.equals("locked")){
                            node.setLock(user);
                        }
                    }
                    child = new DefaultMutableTreeNode(node);
                    DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+node.getID());
                    ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, child,0);
                    DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(node.getPath());
                    ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, child,1);
                    ((DefaultTreeModel)tree.getModel()).nodeChanged(child);
                    buildTree(node,child,false);
                }
                model.insertNodeInto(child, root, root.getChildCount());
            }
            optpan.setParent(null,null,false);
            model.reload();
//             sort2(root);
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    /*
     * get from server user that reserved tb
     */
    private String getTBLockedUser(String tbid){
        try{String resp = client.execute("isResourceLocked", new Object[]{tbid}).toString();
            if(resp.equals("false")){
                return "";
            }
            else if (resp.indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"ERROR", resp);
                return "";
            } else {
                return resp;
            }
        } catch (Exception e){
            e.printStackTrace();
            return "";
        }
    }
    
    /*
     * get from server user that reserved tb
     */
    private String getTBReservdUser(String tbid){
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
     * method used to discard and release TB on server
     */
    public boolean discardAndRelease(String tbid){
        try{String resp = client.execute("discardAndReleaseReservedResource", new Object[]{tbid}).toString();
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
                            model.reload(treenode);
                            optpan.setParent(finalnode,treenode,true);
                            remove.setEnabled(false);
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
                    String[] buttons = {"Save","Discard"};
                    String resp = CustomDialog.showButtons(TB.this, JOptionPane.QUESTION_MESSAGE,
                                                            JOptionPane.DEFAULT_OPTION, null,buttons ,
                                                            "Save","Save TB before releasing?");
                    if (!resp.equals("NULL")) {
                        if(resp.equals("Save")){
                            success = saveAndRelease("/"+node.getName());
                            setSavedState(treenode,true);
                            node.setReserved("");
                            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                            optpan.setParent(node,treenode,false);
                        }
                        else if(resp.equals("Discard")){
                            success = discardAndRelease("/"+node.getName());
                            buildFirstLevelTB();
                            optpan.setParent(null,null,false);
                        }
                    } else {
                        success = discardAndRelease("/"+node.getName());
                        buildFirstLevelTB();
                        optpan.setParent(null,null,false);
                    }
                }
                if(success){   
                    add.setText("Add TB");
                }
            }});
        p.add(item);
        if(!reserved.equals(RunnerRepository.user))item.setEnabled(false);
        item = new JMenuItem("Discard Changes & Release");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent evnt){
                startProgressBar(ev.getXOnScreen(),ev.getYOnScreen());
                new Thread(){
                    public void run(){
                        if(discardAndRelease("/"+node.getName())){
                            setSavedState(treenode,true);
                            add.setText("Add TB");
                            buildFirstLevelTB();
                            optpan.setParent(null,null,false);
                            progress.dispose();
                            
                        }                       
                    }
                }.start();
            }});
        p.add(item);
        if(getSavedState(treenode)){
            item.setEnabled(false);
        }
        if(!reserved.equals(RunnerRepository.user))item.setEnabled(false);
        if(PermissionValidator.canChangeTBLock()&&reserved.equals("")){
            item = new JMenuItem("Lock");
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    try{String resp = client.execute("lockResource", new Object[]{"/"+node.getName()}).toString();
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
                    try{String resp = client.execute("unlockResource", new Object[]{"/"+node.getName()}).toString();
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
                if(saveChanges("/"+node.getName())){
                    setSavedState(treenode,true);
                }}});
        p.add(item);
        if(getSavedState(treenode)){
            item.setEnabled(false);
        }
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
            int size = root.getChildCount();
            for(int i=0;i<size;i++){
                if(resp.equals(((Node)((DefaultMutableTreeNode)root.getChildAt(i)).getUserObject()).getName())){
                    CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,TB.this,"Warning", 
                                        "There is a TB with the same name, please use different name.");
                    return;
                }
            }
            try{
                Node newnode = new Node(null,resp,resp,parent,null,(byte)0);
                resp = client.execute("setResource", new Object[]{resp,"/","{}"}).toString();
                if(resp.indexOf("*ERROR*")==-1){                        
                    parent.addChild(resp, newnode);
                    newnode.setID(resp);
                    DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(newnode);
                    DefaultMutableTreeNode root = (DefaultMutableTreeNode)((DefaultTreeModel)tree.getModel()).getRoot();
                    
                    size = root.getChildCount();//prepare for sorting
                    String [] names = new String[size+1];//names to sort
                    DefaultMutableTreeNode childnode;
                    for(int i=0;i<size;i++){
                        childnode = (DefaultMutableTreeNode)root.getChildAt(i);
                        names[i] = ((Node)childnode.getUserObject()).getName();
                    }
                    names[size] = newnode.getName();
                    Arrays.sort(names);
                    for(int i=0;i<size+1;i++){
                        if(names[i].equals(newnode.getName())){
                            ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, root, i);
                            break;
                        }
                    }
                    
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
                    resp = client.execute("setResource", new Object[]{resp,"/"+parent.getPath().getPath()+"/","{}"}).toString();
                    if(resp.indexOf("*ERROR*")==-1){
                        parent.addChild(resp,newnode);
                        setSavedState(treenode,false);
                        newnode.setID(resp);
                        DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(newnode);
                        
                        int size = treenode.getChildCount();//prepare for sorting
                        String [] names = new String[size+1];//names to sort
                        DefaultMutableTreeNode childnode;
                        for(int i=0;i<size;i++){
                            childnode = (DefaultMutableTreeNode)treenode.getChildAt(i);
                            if(!(childnode.getUserObject() instanceof Node)) names[i]="";
                            else names[i] = ((Node)childnode.getUserObject()).getName();
                        }
                        names[size] = newnode.getName();
                        Arrays.sort(names);
                        for(int i=0;i<size+1;i++){
                            if(names[i].equals(newnode.getName())){
                                ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, treenode, i);
                                break;
                            }
                        }
                        
                        DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+newnode.getID());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treechild,0);
                        DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(newnode.getPath());
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treechild,1);
                    } else {
                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,TB.this,"Error", resp);
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
        try{
            //String id = "/"+node.getName();
            String id = node.getID();
            String s = client.execute("deleteResource", new Object[]{id}).toString();
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
            //construct hash and array for sorting
            Iterator iter = node.getChildren().keySet().iterator();
            String nodesnames [] = new String[node.getChildren().keySet().size()];//names array
            HashMap <String, Node> hash = new HashMap();//hash with name -> nodes
            int index = 0;
            Node child;
            while(iter.hasNext()){
                String childid = iter.next().toString();
                child = getTB(childid,node);
                nodesnames[index] = child.getName();
                hash.put(nodesnames[index], child);
                index++;
            }
            Arrays.sort(nodesnames);//sort by name
            for(String name:nodesnames){
                child = hash.get(name);
                String childid = child.getID();
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
//             Iterator iter = node.getChildren().keySet().iterator();
//             while(iter.hasNext()){
//                 String childid = iter.next().toString();
//                 Node child = getTB(childid,node);
//                 node.addChild(childid, child);
//                 DefaultMutableTreeNode treechild = new DefaultMutableTreeNode(child);
//                 ((DefaultTreeModel)tree.getModel()).insertNodeInto(treechild, treenode,treenode.getChildCount());
//                 if(!onlyfirstlevel){
//                     DefaultMutableTreeNode temp = new DefaultMutableTreeNode("ID: "+child.getID());
//                     ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp, treechild,0);
//                     DefaultMutableTreeNode temp2 = new DefaultMutableTreeNode(child.getPath());
//                     ((DefaultTreeModel)tree.getModel()).insertNodeInto(temp2, treechild,1);
//                     buildTree(child,treechild,onlyfirstlevel);
//                 }
//             }
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
        Object ob = null;
        try{ob = client.execute("getResource", new Object[]{id});
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
            if(!id.equals("/"))id = hash.get("id").toString();
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
            System.out.println("requested id: "+id+" server respons: "+ob.toString());
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
    
    
//     private void sortTree(DefaultMutableTreeNode root) {
//         Enumeration e = root.depthFirstEnumeration();
//         while(e.hasMoreElements()) {
//             DefaultMutableTreeNode node = (DefaultMutableTreeNode)e.nextElement();
//             if(!node.isLeaf()) {
//                 sort2(node);   //selection sort
//               //sort3(node); //iterative merge sort
//             }
//         }
//     }
    
//     Comparator tnc = new Comparator();
//         
//         @Override public int compare(DefaultMutableTreeNode a, DefaultMutableTreeNode b) {
//             //Sort the parent and child nodes separately:
//             if(a.isLeaf() && !b.isLeaf()) {
//                 return 1;
//             }else if(!a.isLeaf() && b.isLeaf()) {
//                 return -1;
//             }else{
//                 String sa = a.getUserObject().toString();
//                 String sb = b.getUserObject().toString();
//                 return sa.compareToIgnoreCase(sb);
//             }
//         }
//     };
    
//     public static void sort2(DefaultMutableTreeNode parent) {
//         TNC tnc = new TNC();
//         int n = parent.getChildCount();
//         for(int i=0;i< n-1;i++) {
//             int min = i;
//             for(int j=i+1;j< n;j++) {
//                 if(tnc.compare((DefaultMutableTreeNode)parent.getChildAt(min),
//                              (DefaultMutableTreeNode)parent.getChildAt(j))>0) {
//                 min = j;
//                 }
//             }
//             if(i!=min) {
//                 MutableTreeNode a = (MutableTreeNode)parent.getChildAt(i);
//                 MutableTreeNode b = (MutableTreeNode)parent.getChildAt(min);
//                 parent.insert(b, i);
//                 parent.insert(a, min);
//             }
//         }
//     }
    
    
}

// class TNC implements Comparator{
//     
//     public int compare(DefaultMutableTreeNode a, DefaultMutableTreeNode b) {
//         //Sort the parent and child nodes separately:
//         if(a.isLeaf() && !b.isLeaf()) {
//             return 1;
//         }else if(!a.isLeaf() && b.isLeaf()) {
//             return -1;
//         }else{
//             String sa = a.getUserObject().toString();
//             String sb = b.getUserObject().toString();
//             return sa.compareToIgnoreCase(sb);
//         }
//     }
//     
//     public int compare(Object ob1,Object ob2){
//         return -1;
//     }
// }


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
    
    protected Transferable createTransferable(JComponent c) {  
        JTree tree = (JTree)c;  
        TreePath[] paths = tree.getSelectionPaths();  
        if(paths != null) {  
            // Make up a node array of copies for transfer and  
            // another for/of the nodes that will be removed in  
            // exportDone after a successful drop.  
            List<Node> copies =  new ArrayList<Node>();   
            DefaultMutableTreeNode node =  (DefaultMutableTreeNode)paths[0].getLastPathComponent();  
            Node copy = copy((Node)node.getUserObject());
            copies.add(copy);  
            for(int i = 1; i < paths.length; i++) {  
                DefaultMutableTreeNode next =  
                    (DefaultMutableTreeNode)paths[i].getLastPathComponent();  
                // Do not allow higher level nodes to be added to list.  
                if(next.getLevel() < node.getLevel()) {  
                    break;  
                } else if(next.getLevel() > node.getLevel()) {  // child node  
                } else {                                        // sibling  
                    copies.add(copy((Node)next.getUserObject()));  
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
   
    public int getSourceActions(JComponent c) {  
        return MOVE;  
    }  
   
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

