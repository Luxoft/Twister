/*
File: ConfigTree.java ; This file is part of Twister.
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

public class ConfigTree extends JPanel{
    private ConfigEditor confeditor;
    public JTree tree;
    private DefaultMutableTreeNode root;
    public ChannelSftp connection;
    public Session session;
    
    public ConfigTree(){
        JPanel buttons = new JPanel();
        JButton nfile = new JButton("New File");
        JButton ndir = new JButton("New Directory");
        JButton remfile = new JButton("Remove");
        buttons.add(nfile);
        buttons.add(ndir);
        buttons.add(remfile);
        remfile.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(tree.getModel().isLeaf(tree.getSelectionPath().getLastPathComponent())){
                    String thefile = tree.getSelectionPath().getParentPath().getLastPathComponent().toString()
                                            + "/"
                                            + tree.getSelectionPath().getLastPathComponent().toString();
                    try{connection.rm(thefile);}
                    catch(Exception e){System.out.println("Could not delete: "+thefile);
                                       e.printStackTrace();
                    }
                } else {
                    String thefile = tree.getSelectionPath().getLastPathComponent().toString();
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
        setLayout(new BorderLayout());
        root = new DefaultMutableTreeNode("root", true);
        initializeSftp();
        try{connection.cd(RunnerRepository.getTestConfigPath());
            getList(root,connection,RunnerRepository.getTestConfigPath());}
        catch(Exception e){e.printStackTrace();}
        tree = new JTree(root);
        tree.addTreeSelectionListener(new TreeSelectionListener(){
            public void valueChanged(TreeSelectionEvent ev){
                
                TreePath newPath = ev.getNewLeadSelectionPath(); 
                
                DefaultMutableTreeNode newNode = null;  
                if(newPath != null){
                    newNode = (DefaultMutableTreeNode)newPath.getLastPathComponent(); 
                    if(tree.getModel().isLeaf(newNode)){
                        doubleClicked();
                    }
                }
            }
        });
        
        DefaultTreeModel treemodel = new DefaultTreeModel(root,true);
        tree.setModel(treemodel);
        tree.expandRow(1);
        tree.setRootVisible(false);
        tree.addMouseListener(new MouseAdapter() {
//             public void mouseClicked(MouseEvent ev) {
//                 if(ev.getClickCount()==2){
//                     doubleClicked();
//                 }}
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
//                     if(tree.getSelectionPath()!=null&& tree.getSelectionPaths().length == 1&&
//                         tree.getModel().isLeaf(tree.getSelectionPath().getLastPathComponent())){
//                         item = new JMenuItem("remove");
//                         p.add(item);
//                         item.addActionListener(new ActionListener() {
//                             public void actionPerformed(ActionEvent evnt) {
//                                 removeFile();
//                             }   
//                         });
//                     }
//                     
                    p.show(tree, ev.getX(), ev.getY());
                }
            }
        });
        add(new JScrollPane(tree),BorderLayout.CENTER);
        add(buttons,BorderLayout.SOUTH);
    }
    
    public String [] getFiles(){
        ArrayList<String> a = new ArrayList<String>();
        Enumeration e = root.depthFirstEnumeration();
        DefaultMutableTreeNode element;
        while(e.hasMoreElements()){
            element = (DefaultMutableTreeNode)e.nextElement();
            if(element.isLeaf()){
                a.add(element.getParent().toString()+"/"+element.toString());
            }
        }
        String [] files=new String[a.size()];
        a.toArray(files);
        return files;
    }
    
//     private void removeFile(){
//         String thefile = tree.getSelectionPath().getParentPath()
//                         .getLastPathComponent().toString()
//                         + "/"
//                         + tree.getSelectionPath().getLastPathComponent()
//                                 .toString();
//         if(RunnerRepository.removeRemoteFile(thefile)){
//             refreshStructure();
//         } else {
//             System.out.println("Could not delte remote file: "+thefile);
//         }
//         
//     }
    
    private void removeDirectory(String directory){
        Vector<LsEntry> vector1=null;
        try{vector1 = connection.ls(directory);}
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
                try{connection.rm(directory+"/"+vector1.get(i).getFilename());}
                catch(Exception e){
                    System.out.println("Could not delete file: "+directory+"/"+vector1.get(i).getFilename());
                    e.printStackTrace();
                }
            }
        }
        for(String dir:folders){
            removeDirectory(dir);
        }
        try{connection.rmdir(directory);}
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
    
    public void refreshStructure() {
        try{root.remove(0);}
        catch(Exception e){e.printStackTrace();}
        try {connection.cd(RunnerRepository.getTestConfigPath());
            getList(root,connection,RunnerRepository.getTestConfigPath());;
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
                String thefile = tree.getSelectionPath().getParentPath()
                        .getLastPathComponent().toString()
                        + "/"
                        + tree.getSelectionPath().getLastPathComponent()
                                .toString();
                File file = new File(RunnerRepository.temp+RunnerRepository.getBar()+
                                    "Twister"+RunnerRepository.getBar()+"XML"+
                                    RunnerRepository.getBar()+
                                    tree.getSelectionPath().getLastPathComponent()
                                    .toString());
                try{String content = RunnerRepository.getRemoteFileContent(thefile);
                    BufferedWriter writer = new BufferedWriter(new FileWriter(file));
                    writer.write(content);
                    writer.close();
                    confeditor.reinitialize();
                    confeditor.parseDocument(file);
                    confeditor.setRemoteLocation(tree.getSelectionPath().getParentPath()
                                                    .getLastPathComponent().toString());
                    confeditor.buildTree();
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
    
    public void getList(DefaultMutableTreeNode node, ChannelSftp c, String curentdir) {
        try {
            DefaultMutableTreeNode child = new DefaultMutableTreeNode(curentdir,true);
            Vector<LsEntry> vector1 = c.ls(".");
            Vector<String> vector = new Vector<String>();
            Vector<String> folders = new Vector<String>();
            Vector<String> files = new Vector<String>();
            int lssize = vector1.size();
            if (lssize >= 2) {
                node.add(child);
            }
            String current;
            for (int i = 0; i < lssize; i++) {
                if (vector1.get(i).getFilename().split("\\.").length == 0){
                    continue;
                }
                if(vector1.get(i).getAttrs().isDir()){
                    folders.add(vector1.get(i).getFilename());
                } else {
                    files.add(vector1.get(i).getFilename());
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
                    getList(child, c,curentdir+"/"+vector.get(i));
                    c.cd(current);
                } catch (SftpException e) {
                    if (e.id == 4) {
                        DefaultMutableTreeNode  child2 = new DefaultMutableTreeNode(vector.get(i),false);
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