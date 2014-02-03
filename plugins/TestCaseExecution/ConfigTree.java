/*
File: ConfigTree.java ; This file is part of Twister.
Version: 2.007

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
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.JTree;
import javax.swing.JScrollPane;
import java.awt.BorderLayout;
import com.jcraft.jsch.ChannelSftp;
import java.util.Vector;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import java.util.Collections;
import com.jcraft.jsch.SftpException;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import java.util.Properties;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.io.BufferedWriter;
import java.io.FileWriter;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JFrame;
import javax.swing.JProgressBar;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.JButton;
import javax.swing.JTextField;
import javax.swing.AbstractAction;
import java.io.OutputStream;
import com.twister.MySftpBrowser;
import javax.swing.event.TreeSelectionListener;
import javax.swing.event.TreeSelectionEvent;
import javax.swing.tree.TreePath;
import java.util.Enumeration;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;
import javax.xml.bind.DatatypeConverter;
import com.twister.CustomDialog;
import javax.swing.JOptionPane;
import javax.swing.tree.TreeNode;



public class ConfigTree extends JPanel{
    private ConfigEditor confeditor;
    public JTree tree;
    private DefaultMutableTreeNode root;
    public ChannelSftp connection;
    public Session session;
    
    public ConfigTree(){
        JPanel buttons = new JPanel();
        JButton nfile = new JButton("New");
        final JButton open = new JButton("Open");
        JButton ndir = new JButton("MkDir");
        final JButton remfile = new JButton("Delete");
        JButton refresh = new JButton("Refresh");
        buttons.add(nfile);
        buttons.add(open);
        buttons.add(remfile);
        buttons.add(ndir);
        buttons.add(refresh);
        open.setEnabled(false);
        remfile.setEnabled(false);
        remfile.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                Object [] path = tree.getSelectionPath().getPath();
                StringBuilder sb = new StringBuilder();
                for(int i=2;i<path.length-1;i++){
                    sb.append(path[i].toString());
                    sb.append("/");
                }
                String user = "";
                String filename = path[path.length-1].toString();
                if(path[path.length-1].toString().indexOf(" - Reserved by ")!=-1){
                    String [] temp = path[path.length-1].toString().split(" - Reserved by ");
                    filename = temp[0];
                    if(temp.length>1)user = temp[1];
                }
                sb.append(filename);
                String thefile = sb.toString();
                if(!((DefaultMutableTreeNode)tree.getSelectionPath().getLastPathComponent()).getAllowsChildren()){
//                     String thefile = tree.getSelectionPath().getParentPath().getLastPathComponent().toString()
//                                             + "/"
//                                             + tree.getSelectionPath().getLastPathComponent().toString();
                    
                    
                    try{
                        
//                         Object [] path = tree.getSelectionPath().getPath();
//                         StringBuilder sb = new StringBuilder();
//                         for(int i=1;i<path.length-1;i++){
//                             sb.append(path[i].toString());
//                             sb.append("/");
//                         }
//                         String user = "";
//                         String filename = path[path.length-1].toString();
//                         if(path[path.length-1].toString().indexOf(" - Reserved by ")!=-1){
//                             String [] temp = path[path.length-1].toString().split(" - Reserved by ");
//                             filename = temp[0];
//                             if(temp.length>1)user = temp[1];
//                         }
//                         sb.append(filename);
//                         String thefile = sb.toString();
                        
                        
                        
                        String content = RunnerRepository.getRPCClient().execute("deleteConfigFile", new Object[]{thefile}).toString();
                        if(content.indexOf("*ERROR*")!=-1){
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigTree.this,"ERROR", content);
                        }
//                         connection.rm(thefile);
                    }
                    catch(Exception e){System.out.println("Could not delete: "+thefile);
                                       e.printStackTrace();
                    }
                } else {
//                     String thefile = tree.getSelectionPath().getLastPathComponent().toString();
                    try{removeDirectory(thefile);}
                    catch(Exception ex){System.out.println("Could not delete: "+thefile);
                                        ex.printStackTrace();
                    }
                }
                refreshStructure();
            }
        });
        nfile.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                final JTextField tf = new JTextField();
                try{tf.setText(RunnerRepository.getTestConfigPath());
                }catch(Exception e){
                    e.printStackTrace();
                }
                AbstractAction action = new AbstractAction(){
                    public void actionPerformed(ActionEvent ev){
                        try{OutputStream os = connection.put(tf.getText());
                            os.close();
                            refreshStructure();
                            Enumeration enumeration = root.depthFirstEnumeration();
                            while (enumeration.hasMoreElements()) {
                              DefaultMutableTreeNode node = (DefaultMutableTreeNode) enumeration.nextElement();
                              if((node.getParent()+"/"+node).toString().equals(tf.getText())){
                                  tree.setSelectionPath(new TreePath(((DefaultTreeModel)tree.getModel()).getPathToRoot(node)));
                              }
                            }
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                };
                new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,tf,ConfigTree.this,false).setAction(action);
            }
        });
        ndir.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                final JTextField tf = new JTextField();
                try{
                    tf.setText(RunnerRepository.getTestConfigPath());
                }catch(Exception e){
                    e.printStackTrace();
                }
                AbstractAction action = new AbstractAction(){
                    public void actionPerformed(ActionEvent ev){
                        try{connection.mkdir(tf.getText());
                            refreshStructure();
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                };
                MySftpBrowser browser = new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,tf,ConfigTree.this,false);
                browser.setAction(action);
                browser.setFieldName("Directory name:");
//                 new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,tf,ConfigTree.this,true).setAction(action);
            }
        });
        
        refresh.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                refreshStructure();
            }
        });
        open.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                doubleClicked();
            }
        });
        setLayout(new BorderLayout());
        root = new DefaultMutableTreeNode("root", true);
        initializeSftp();
//         try{
            //connection.cd(RunnerRepository.getTestConfigPath());
            //getList(root,connection,RunnerRepository.getTestConfigPath());
            
            //refreshStructure();
            
//         }catch(SftpException e){
//             if(e.id==ChannelSftp.SSH_FX_NO_SUCH_FILE){
//                 System.out.println("Could not get:"+RunnerRepository.getPredefinedSuitesPath());
//             }
//         } catch (Exception e) {
//             e.printStackTrace();
//         }
        tree = new JTree(root);
        tree.addTreeSelectionListener(new TreeSelectionListener(){
            public void valueChanged(TreeSelectionEvent ev){
                
                TreePath newPath = ev.getNewLeadSelectionPath(); 
                
                DefaultMutableTreeNode newNode = null;  
                if(newPath != null){
                    remfile.setEnabled(true);
                    newNode = (DefaultMutableTreeNode)newPath.getLastPathComponent(); 
                    if(!newNode.getAllowsChildren()){
                        //doubleClicked();
                        open.setEnabled(true);
//                         remfile.setEnabled(true);
                    } else {
                        open.setEnabled(false);
//                         remfile.setEnabled(false);
                    }
                }
            }
        });
        
        DefaultTreeModel treemodel = new DefaultTreeModel(root,true);
        tree.setModel(treemodel);
        tree.expandRow(1);
        tree.setRootVisible(false);
        tree.addMouseListener(new MouseAdapter() {
            public void mouseReleased(final MouseEvent ev){
                if (ev.isPopupTrigger()) {
                    JPopupMenu p = new JPopupMenu();
                    JMenuItem item = new JMenuItem("Refresh tree");
                    p.add(item);
                    item.addActionListener(new ActionListener() {
                        public void actionPerformed(ActionEvent evnt) {
                            refreshTree(ev.getX(),ev.getY());
                        }   
                    });
                    p.show(tree, ev.getX(), ev.getY());
                }
            }
        });
        add(new JScrollPane(tree),BorderLayout.CENTER);
        JPanel temp = new JPanel();
        temp.setLayout(new BorderLayout());
        temp.add(buttons, BorderLayout.WEST);
        add(temp,BorderLayout.SOUTH);
        refreshStructure();
    }
    
    public String [] getFiles(){
        ArrayList<String> a = new ArrayList<String>();
        Enumeration e = root.depthFirstEnumeration();
        DefaultMutableTreeNode element;
        while(e.hasMoreElements()){
            element = (DefaultMutableTreeNode)e.nextElement();
            if(!element.getAllowsChildren()){
                TreeNode[] tp = element.getPath();
                if(tp.length<2)continue;
                StringBuilder sb = new StringBuilder();
                for(int i=2;i<tp.length-1;i++){
                    sb.append(tp[i].toString());
                    sb.append("/");
                }
                String file = tp[tp.length-1].toString().split("- Reserved by ")[0];
                sb.append(file);
                a.add(sb.toString());
            }
        }
        String [] files=new String[a.size()];
        a.toArray(files);
        return files;
    }
    
    public void releaseAll(){
        RunnerRepository.window.mainpanel.p4.getTestConfig().cfgedit.close.doClick();
        ArrayList<String> a = new ArrayList<String>();
        Enumeration e = root.depthFirstEnumeration();
        DefaultMutableTreeNode element;
        while(e.hasMoreElements()){
            element = (DefaultMutableTreeNode)e.nextElement();
            if(!element.getAllowsChildren()){
                TreeNode[] tp = element.getPath();
                if(tp.length<2)continue;
                StringBuilder sb = new StringBuilder();
                for(int i=2;i<tp.length-1;i++){
                    sb.append(tp[i].toString());
                    sb.append("/");
                }
                String str[] = tp[tp.length-1].toString().split("- Reserved by ");
                if(str.length==2&&str[1].equals(RunnerRepository.user)){
                    sb.append(str[0]);
                    try{System.out.println("unlocking cfg: "+sb.toString());
                        RunnerRepository.getRPCClient().execute("unlockConfig", new Object[]{sb.toString()}).toString();}
                    catch(Exception ex){ex.printStackTrace();}
                }
            }
        }
    }
    
    public void disconnect(){
        connection.disconnect();
        session.disconnect();
    }

    
    private void removeDirectory(String directory){
        System.out.println(directory);
        Vector<LsEntry> vector1=null;
        try{vector1 = connection.ls(RunnerRepository.TESTCONFIGPATH+"/"+directory);}
        catch(Exception e){e.printStackTrace();}
        Vector<String> vector = new Vector<String>();
        Vector<String> folders = new Vector<String>();
        Vector<String> files = new Vector<String>();
        int lssize = vector1.size();
        for (int i = 0; i < lssize; i++) {
            if (vector1.get(i).getFilename().split("\\.").length == 0){
                continue;
            }
            if(vector1.get(i).getAttrs().isDir()){
                folders.add(directory+"/"+vector1.get(i).getFilename());
            } else {
                
                try{String content = RunnerRepository.getRPCClient().execute("deleteConfigFile", new Object[]{directory+"/"+vector1.get(i).getFilename()}).toString();
                    if(content.indexOf("*ERROR*")!=-1){
                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigTree.this,"ERROR", content);
                        return;
                    }
                } catch(Exception e){
                    CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigTree.this,"ERROR", "Could not delete file:"+directory+"/"+vector1.get(i).getFilename());
                    e.printStackTrace();
                    return;
                }
                
//                 try{connection.rm(directory+"/"+vector1.get(i).getFilename());}
//                 catch(Exception e){
//                     System.out.println("Could not delete file: "+directory+"/"+vector1.get(i).getFilename());
//                     e.printStackTrace();
//                 }
            }
        }
        for(String dir:folders){
            removeDirectory(dir);
        }
        try{connection.rmdir(RunnerRepository.TESTCONFIGPATH+"/"+directory);}
        catch(Exception e){
                    System.out.println("Could not delete directory: "+directory);
                    e.printStackTrace();
        }
    }

    private void refreshTree(final int X, final int Y) {
        new Thread() {
            public void run() {
                JFrame progress = new JFrame();
                progress.setAlwaysOnTop(true);
                progress.setLocation(X,Y);
                progress.setUndecorated(true);
                JProgressBar bar = new JProgressBar();
                bar.setIndeterminate(true);
                progress.add(bar);
                progress.pack();
                progress.setVisible(true);
                refreshStructure();
                progress.dispose();
            }
        }.start();
    }
    
    public void relseaseConfig(String remotelocation){
        String [] path = remotelocation.split("/");
        DefaultMutableTreeNode node = (DefaultMutableTreeNode)root.getFirstChild();
        for(String el:path){
            if(node==null)break;
            node = findInNode(node,el);
        }
        if(node!=null){
            System.out.println(node.toString());
        } else {
            System.out.println("is null");
        }
    }
    
    private DefaultMutableTreeNode findInNode(DefaultMutableTreeNode node, String name){
        if(node==null)return null;
        int nr = node.getChildCount();
        String compare = "";
        for(int i=0;i<nr;i++){
            compare = ((DefaultMutableTreeNode)node.getChildAt(i)).toString().split(" - Reserved by ")[0];
            if(compare.equalsIgnoreCase(name)){
                return (DefaultMutableTreeNode)node.getChildAt(i);
            }
        }
        return null;
    }
    
    public void refreshStructure() {
        if(root.getChildCount()>0)root.remove(0);
        try{HashMap struct = (HashMap)RunnerRepository.getRPCClient().execute("listConfigs", new Object[]{RunnerRepository.user});
            getList(root,struct);
        } catch (Exception e) {
            e.printStackTrace();
        }
        ((DefaultTreeModel) tree.getModel()).reload();
        tree.expandRow(0);
    }
    
    public void setConfigEditor(ConfigEditor confeditor){
        this.confeditor = confeditor;
    }
    
    private void doubleClicked(){
        if ((tree.getSelectionPaths()!=null) &&
            (tree.getSelectionPaths().length == 1) &&
            (tree.getModel().isLeaf(tree.getSelectionPath()
                            .getLastPathComponent()))) {
            try{
                Object [] path = tree.getSelectionPath().getPath();
                RunnerRepository.window.mainpanel.p4.getTestConfig().cfgedit.close.doClick();
                StringBuilder sb = new StringBuilder();
                for(int i=2;i<path.length-1;i++){
                    sb.append(path[i].toString());
                    sb.append("/");
                }
                String user = "";
                String filename = path[path.length-1].toString();
                if(path[path.length-1].toString().indexOf(" - Reserved by ")!=-1){
                    String [] temp = path[path.length-1].toString().split(" - Reserved by ");
                    filename = temp[0];
                    if(temp.length>1)user = temp[1];
                }
                sb.append(filename);
                String thefile = sb.toString();
                File file = new File(RunnerRepository.temp+RunnerRepository.getBar()+
                                    "Twister"+RunnerRepository.getBar()+"XML"+
                                    RunnerRepository.getBar()+
                                    tree.getSelectionPath().getLastPathComponent()
                                    .toString());
                try{
                    boolean edit = false;
                    if(user.equals("")||user.equals(RunnerRepository.user))edit = true;
                    if(edit){
                        String content = RunnerRepository.getRPCClient().execute("lockConfig", new Object[]{thefile}).toString();
                        if(content.toLowerCase().equals("true")){
//                             refreshStructure();
                            ((DefaultMutableTreeNode)path[path.length-1]).setUserObject(filename+" - Reserved by "+RunnerRepository.user);
                            ((DefaultTreeModel)tree.getModel()).nodeChanged(((DefaultMutableTreeNode)path[path.length-1]));
                            
                        } else {
                            if(content.indexOf("*ERROR*")!=-1){
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigTree.this,"ERROR", content);
                            }
                            edit = false;
                        }
                    }
                    String content = RunnerRepository.getRPCClient().execute("readConfigFile", new Object[]{thefile}).toString();
                    content = new String(DatatypeConverter.parseBase64Binary(content));
                    if(content.indexOf("*ERROR*")!=-1){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,ConfigTree.this,"ERROR", content);
                    }
                    BufferedWriter writer = new BufferedWriter(new FileWriter(file));
                    writer.write(content);
                    writer.close();
                    confeditor.reinitialize();
                    confeditor.parseDocument(file);
                    confeditor.setRemoteLocation(thefile);
                    confeditor.buildTree();
                    RunnerRepository.window.mainpanel.p4.getTestConfig().cfgedit.openedConfig(edit);
                    RunnerRepository.window.mainpanel.p4.getTestConfig().cfgedit.getBinding(thefile);
                    RunnerRepository.window.mainpanel.p4.getTestConfig().cfgedit.interpretBinding();
                }
                catch(Exception e){
                    e.printStackTrace();
                    System.out.println("Could not get :"+thefile+"  file");
                }
            } catch (Exception e){
                e.printStackTrace();
            }
        }
    }
    
    public void getList(DefaultMutableTreeNode parent,HashMap currentelem) {
        try{
            Object ob = currentelem.get("folder");
            boolean folder = false;
            if(ob!=null){
                folder = true;
            }
            
            DefaultMutableTreeNode child = new DefaultMutableTreeNode(currentelem.get("data").toString(),folder);
            parent.add(child);
            
            
            if(!folder){
                Object [] path = child.getPath();
                StringBuilder sb = new StringBuilder();
                for(int i=2;i<path.length;i++){
                    sb.append(path[i].toString());
                    sb.append("/");
                }
                sb.deleteCharAt(sb.length()-1);
                String thefile = sb.toString();
                System.out.println(thefile);
                try{
                    String content = RunnerRepository.getRPCClient().execute("isLockConfig", new Object[]{thefile}).toString();
                    if(!content.toLowerCase().equals("false")){
                        child.setUserObject(currentelem.get("data").toString()+" - Reserved by "+content);
                    }
                }
                catch(Exception e){
                    e.printStackTrace();
                }
            }
            
            
            
            Object [] children = (Object [])currentelem.get("children");
            if(folder&&children!=null&&children.length>0){
                for(Object subchild:children){
                    getList(child,(HashMap)subchild);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
//     public void getList(DefaultMutableTreeNode node, ChannelSftp c, String curentdir) {
//         try {
//             DefaultMutableTreeNode child = new DefaultMutableTreeNode(curentdir,true);
//             Vector<LsEntry> vector1 = c.ls(".");
//             Vector<String> vector = new Vector<String>();
//             Vector<String> folders = new Vector<String>();
//             Vector<String> files = new Vector<String>();
//             int lssize = vector1.size();
//             if (lssize >= 2) {
//                 node.add(child);
//             }
//             String current;
//             for (int i = 0; i < lssize; i++) {
//                 if (vector1.get(i).getFilename().split("\\.").length == 0){
//                     continue;
//                 }
//                 if(vector1.get(i).getAttrs().isDir()){
//                     folders.add(vector1.get(i).getFilename());
//                 } else {
//                     files.add(vector1.get(i).getFilename());
//                 }
//             }
//             Collections.sort(folders);
//             Collections.sort(files);
//             for (int i = 0; i < folders.size(); i++) {
//                 vector.add(folders.get(i));
//             }
//             for (int i = 0; i < files.size(); i++) {
//                 vector.add(files.get(i));
//             }
//             for (int i = 0; i < vector.size(); i++) {
//                 try {
//                     current = c.pwd();
//                     c.cd(vector.get(i));
//                     getList(child, c,curentdir+"/"+vector.get(i));
//                     c.cd(current);
//                 } catch (SftpException e) {
//                     if (e.id == 4) {
//                         DefaultMutableTreeNode  child2 = new DefaultMutableTreeNode(vector.get(i),false);
//                         child.add(child2);
//                     } else {
//                         e.printStackTrace();
//                     }
//                 }
//             }
//         } catch (Exception e) {
//             e.printStackTrace();
//         }
//     }
    
    private void initializeSftp(){
        try{
            JSch jsch = new JSch();
            session = jsch.getSession(RunnerRepository.user, RunnerRepository.host, 22);
            session.setPassword(RunnerRepository.password);
            Properties config = new Properties();
            config.put("StrictHostKeyChecking", "no");
            session.setConfig(config);
            session.connect();
            Channel channel = session.openChannel("sftp");
            channel.connect();
            connection = (ChannelSftp)channel;
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}