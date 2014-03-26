/*
File: ConfigTree.java ; This file is part of Twister.
Version: 2.015

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
import java.util.Vector;
import java.util.Collections;
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
import java.io.FileInputStream;
import javax.xml.bind.DatatypeConverter;



public class ConfigTree extends JPanel{
    private ConfigEditor confeditor;
    public JTree tree;
    private DefaultMutableTreeNode root;
    
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
                for(int i=1;i<path.length-1;i++){
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
                    try{
                        String content = RunnerRepository.getRPCClient().execute("deleteConfigFile", new Object[]{thefile}).toString();
                        if(content.indexOf("*ERROR*")!=-1){
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigTree.this,"ERROR", content);
                        }
                        refreshStructure();
                    }
                    catch(Exception e){System.out.println("Could not delete: "+thefile);
                                       e.printStackTrace();
                    }
                } else {
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
                        try{System.out.println("Creating: "+tf.getText());                       
                            String content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<root>\n</root>\n";
                            content = DatatypeConverter.printBase64Binary(content.getBytes());
                            if(RunnerRepository.window.mainpanel.p4.getPlugins().isClearCaseEnabled()){
                                RunnerRepository.getRPCClient().execute("writeFile", new Object[]{tf.getText(),content,"w","clearcase:TestConfigPath"}).toString();
                            } else {
                                RunnerRepository.getRPCClient().execute("writeFile", new Object[]{tf.getText(),content,"w"}).toString();
                            }
                            refreshStructure();
                            Enumeration enumeration = root.depthFirstEnumeration();
                            while (enumeration.hasMoreElements()) {
                              DefaultMutableTreeNode node = (DefaultMutableTreeNode) enumeration.nextElement();
                              if((node.getParent()+"/"+node).toString().equals(tf.getText())){
                                  tree.setSelectionPath(new TreePath(((DefaultTreeModel)tree.getModel()).getPathToRoot(node)));
                              }
                            }
                        } catch(Exception e){
                            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigTree.this,"ERROR", "Could not write file! Check log.");
                            System.out.println("Could not upload:"+tf.getText());
                            e.printStackTrace();
                        }
                    }
                };
                MySftpBrowser browser = new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,RunnerRepository.CENTRALENGINEPORT,tf,ConfigTree.this,false);
                browser.setAction(action);
                if(RunnerRepository.window.mainpanel.p4.getPlugins().isClearCaseEnabled()){
                    browser.setTag("TestConfigPath");
                }
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
                        try{RunnerRepository.createRemoteDir(tf.getText());
                            refreshStructure();
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                };
                MySftpBrowser browser = new MySftpBrowser(RunnerRepository.host,RunnerRepository.user,RunnerRepository.password,RunnerRepository.CENTRALENGINEPORT,tf,ConfigTree.this,false);
                browser.setAction(action);
                if(RunnerRepository.window.mainpanel.p4.getPlugins().isClearCaseEnabled()){
                    browser.setTag("TestConfigPath");
                }
                browser.setFieldName("Directory name:");
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
//         initializeSftp();
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
        //temp.setLayout(new BorderLayout());
        //temp.add(buttons, BorderLayout.WEST);
        temp.add(buttons);
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
                for(int i=1;i<tp.length-1;i++){
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
                    try{RunnerRepository.getRPCClient().execute("unlockConfig", new Object[]{sb.toString()}).toString();}
                    catch(Exception ex){ex.printStackTrace();}
                }
            }
        }
    }
    
    private void removeDirectory(String directory){
        try{
            if(RunnerRepository.window.mainpanel.p4.getPlugins().isClearCaseEnabled()){
                String respons = RunnerRepository.getRPCClient().execute("findCcXmlTag", new Object[]{"TestConfigPath"}).toString();
                if(respons.indexOf("*ERROR*")!=-1){
                    CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigTree.this,"ERROR", respons);
                    return;
                }
                RunnerRepository.deleteRemoteDir(respons.split(":")[1]+"/"+directory,"TestConfigPath");
            } else {
                RunnerRepository.deleteRemoteDir(RunnerRepository.getTestConfigPath()+"/"+directory,null);
            }
            refreshStructure();
        } catch(Exception e){
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
    
    public void releaseConfig(String remotelocation){
        String [] path = remotelocation.split("/");
        DefaultMutableTreeNode node = root;
        for(String el:path){
            if(node==null)break;
            node = findInNode(node,el);
        }
        if(node!=null){
            node.setUserObject(node.toString().split(" - Reserved by ")[0]);
            ((DefaultTreeModel)tree.getModel()).nodeChanged(node);
        } else {
            System.out.println("Could not find: "+remotelocation);
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
        if(root.getChildCount()>0)root.removeAllChildren();
        Object ob = null;
        try{ob = RunnerRepository.getRPCClient().execute("listConfigs", new Object[]{RunnerRepository.user});
            HashMap struct = (HashMap)ob;
            Object [] children = (Object [])struct.get("children");
            if(children!=null&&children.length>0){
                for(Object subchild:children){
                    getList(root,(HashMap)subchild);
                }
            }
            //getList(root,struct);
        } catch (Exception e) {
            if(ob.toString().indexOf("*ERROR*")!=-1)CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigTree.this,"ERROR", ob.toString());
            System.out.println("Server response: "+ob.toString());
            e.printStackTrace();
        }
        ((DefaultTreeModel) tree.getModel()).reload();
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
                for(int i=1;i<path.length-1;i++){
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
                        String content = "true";
                        if(!user.equals(RunnerRepository.user))content = RunnerRepository.getRPCClient().execute("lockConfig", new Object[]{thefile}).toString();
                        if(content.toLowerCase().equals("true")){
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
                    if(content.indexOf("*ERROR*")!=-1){
                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ConfigTree.this,"ERROR", content);
                    }
                    content = new String(DatatypeConverter.parseBase64Binary(content));
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
    
    private void getList(DefaultMutableTreeNode parent,HashMap currentelem) {
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
                for(int i=1;i<path.length;i++){
                    sb.append(path[i].toString());
                    sb.append("/");
                }
                sb.deleteCharAt(sb.length()-1);
                String thefile = sb.toString();
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
    
//     private void initializeSftp(){
//         try{
//             JSch jsch = new JSch();
//             session = jsch.getSession(RunnerRepository.user, RunnerRepository.host, 22);
//             session.setPassword(RunnerRepository.password);
//             Properties config = new Properties();
//             config.put("StrictHostKeyChecking", "no");
//             session.setConfig(config);
//             session.connect();
//             Channel channel = session.openChannel("sftp");
//             channel.connect();
//             connection = (ChannelSftp)channel;
//         } catch (Exception e){
//             e.printStackTrace();
//         }
//     }
}
