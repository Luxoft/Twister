/*
File: ClearCasePanel.java ; This file is part of Twister.
Version: 2.017

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
import java.awt.EventQueue;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import javax.swing.JScrollPane;
import javax.swing.JTree;
import javax.swing.tree.MutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.DefaultMutableTreeNode;
import java.io.File;
import java.awt.BorderLayout;
import java.awt.dnd.DragSource;
import java.awt.event.MouseAdapter;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseListener;
import java.awt.event.MouseEvent;
import javax.swing.TransferHandler;
import java.awt.dnd.DragSource;
import java.awt.dnd.DropTarget;
import java.awt.dnd.DnDConstants;
import java.awt.dnd.DragGestureListener;
import java.awt.dnd.DragGestureEvent;
import java.awt.dnd.DragSourceListener;
import javax.swing.tree.TreePath;
import java.awt.dnd.DragSourceDropEvent;
import java.awt.dnd.DragSourceDragEvent;
import java.awt.dnd.DragSourceEvent;
import java.awt.dnd.DragSourceContext;
import java.io.IOException;
// import com.jcraft.jsch.ChannelSftp;
// import com.jcraft.jsch.ChannelSftp.LsEntry;
import java.util.Vector;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import javax.xml.parsers.ParserConfigurationException;
import org.xml.sax.SAXException;
import java.io.IOException;
import java.util.Comparator;
import java.util.Collections;
// import com.jcraft.jsch.SftpException;
import java.net.URL;
import java.net.URLConnection;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Scanner;
import java.awt.Container;
import javax.swing.tree.TreeModel;
import java.awt.Dimension;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import javax.swing.JTextArea;
import javax.swing.JFrame;
import javax.swing.JButton;
import java.awt.BorderLayout;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import java.awt.event.MouseMotionAdapter;
import javax.swing.text.PlainDocument;
import java.io.FileReader;
import javax.swing.InputMap;
import javax.swing.JComponent;
import javax.swing.KeyStroke;
import java.awt.event.KeyEvent;
import java.awt.event.InputEvent;
import java.awt.event.KeyAdapter;
import javax.swing.JProgressBar;
import com.google.gson.JsonObject;
import javax.swing.SwingUtilities;
import javax.swing.JOptionPane;
import java.util.Iterator;
import java.util.Map.Entry;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JFileChooser;
import javax.swing.BorderFactory;
import java.awt.Color;
import java.awt.Dimension;
import com.google.gson.JsonPrimitive;
import javax.swing.JComboBox;
import javax.swing.JCheckBox;
import javax.swing.DefaultComboBoxModel;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import com.twister.Item;
import com.twister.CustomDialog;
import java.util.Properties;
import java.awt.datatransfer.Transferable;
import java.awt.datatransfer.StringSelection;
import java.awt.dnd.DragSourceListener;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.nio.ByteBuffer;
import java.util.HashMap;
import javax.swing.GroupLayout;
import java.io.FileReader;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.JsonArray;
import java.awt.MouseInfo;

public class ClearCasePanel{

    private static final long serialVersionUID = 1L;
    public JTree tree;
    public DefaultMutableTreeNode root;
    private boolean dragging;
    private TreePath[] selected;
    private DefaultMutableTreeNode child2;
    private JEditTextArea textarea;

    public ClearCasePanel() {
        RunnerRepository.introscreen.setStatus("Started ClearCasePanel interface initialization");
        RunnerRepository.introscreen.addPercent(0.035);
        RunnerRepository.introscreen.repaint();
        
        root = new DefaultMutableTreeNode("root", true);
        try {
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        tree = new JTree();
        tree.setModel(new DefaultTreeModel(root,true));
        tree.expandRow(1);
        tree.setTransferHandler(new TransferHandler(){
            
            protected Transferable createTransferable(JComponent c)
            {
                return new StringSelection("clearcase");
            }
            public int getSourceActions(JComponent c)
            {
                return TransferHandler.COPY_OR_MOVE;
            }
        });
        
        tree.addMouseListener(new MouseAdapter() {
            public void mousePressed(MouseEvent ev) {
                treeClick(ev);
            }
            public void mouseReleased(MouseEvent ev) {
                treeClickReleased(ev);
            }
        });
        tree.setDragEnabled(true);
        tree.setRootVisible(false);
        RunnerRepository.introscreen.setStatus("Finished Explorer interface initialization");
        RunnerRepository.introscreen.addPercent(0.035);
        RunnerRepository.introscreen.repaint();
    }

    /*
     * executed on tree released click
     */
    public void treeClickReleased(final MouseEvent ev) {
        if (ev.isPopupTrigger()) {
            String remotefilename ;
            if(tree.getSelectionPath() !=null){
                if(tree.getModel().isLeaf(tree.getSelectionPath()
                            .getLastPathComponent())){
                    remotefilename = tree.getSelectionPath().getPathComponent(
                                        tree.getSelectionPath().getPathCount() - 2)
                                        + "/" + tree.getSelectionPath().getLastPathComponent();
                } else {
                    remotefilename = tree.getSelectionPath().getLastPathComponent().toString();
                }
                HashMap<String, String> hash = new HashMap<String, String>();
                hash.put("command", "cleartool lsco "+remotefilename);
                String response = RunnerRepository.window.mainpanel.getP5().sendCommand(hash,true);
                refreshPopup(ev,response,remotefilename);
            } else {
                refreshPopup(ev,null,null);
            }
        } 
    }

    /*
     * executed on tree click
     */
    public void treeClick(final MouseEvent ev) {
            setDragging(true);
            selected = tree.getSelectionPaths();
            if (selected != null) {
                int left = 0;
                int right = selected.length - 1;
                while (left < right) {
                    TreePath temp = selected[left];
                    selected[left] = selected[right];
                    selected[right] = temp;
                    left++;
                    right--;
                }
            }
//         }
    }

    /*
     * returns the selected paths
     */

    public TreePath[] getSelected() {
        Arrays.sort(selected, new Compare());
        List<TreePath> listOfPaths = Arrays.asList(selected);
        Collections.reverse(listOfPaths);
        selected = listOfPaths.toArray(new TreePath[] {});
        return selected;
    }

    /*
     * popup displayed on tree panel
     */
    public void refreshPopup(final MouseEvent ev,String response,final String remotefilename) {
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Refresh tree");
        p.add(item);
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent evnt) {
                refreshTree(ev.getX(),ev.getY());
            }   
        });
        if(response!=null&&remotefilename!=null){
            item = new JMenuItem("Get TC Description");
            p.add(item);
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    new Thread(){
                        public void run(){
                            if ((tree.getSelectionPaths()!=null) &&
                            (tree.getSelectionPaths().length == 1) &&
                            (tree.getModel().isLeaf(tree.getSelectionPath()
                                            .getLastPathComponent()))) {
                                try {
                                    String thefile = tree.getSelectionPath().getParentPath()
                                            .getLastPathComponent().toString()
                                            + "/"
                                            + tree.getSelectionPath().getLastPathComponent()
                                                    .toString();
                                    System.out.println("thefile: "+thefile);
//                                     HashMap<String,String>hm = new HashMap<String,String>();
//                                     hm.put("command","get_test_description");
//                                     hm.put("file_name",thefile);
//                                     System.out.println("Command get_test_description for "+thefile);
//                                     String result = RunnerRepository.window.mainpanel.getP5().sendCommand(hm,false);
                                    String result = RunnerRepository.getRPCClient().execute(
                                                                                    "getTestDescription", new Object[] { thefile })
                                                                                    + "";
                                    System.out.println("Result: "+result);
                                    Container pan1 = (Container) RunnerRepository.window.mainpanel.p1.splitPane.getComponent(1);
                                    TCDetails pan2 = (TCDetails) pan1.getComponents()[1];
                                    pan2.text.setText(result);
                                } catch (Exception e) {
                                    e.printStackTrace();
                                }
                            }
                        }
                    }.start();
                }
            });
            final String editable;
            if (tree.getSelectionPath()!=null) {
                editable = tree.getSelectionPath().getLastPathComponent() + "";
            } else {
                editable = "";
            }
            if ((tree.getSelectionPath()!=null)&&(tree.getSelectionPaths().length == 1)) {                
                if(response.indexOf("checkout")==-1){
                    item = new JMenuItem("Checkout");
                    p.add(item);
                    item.addActionListener(new ActionListener() {
                        public void actionPerformed(ActionEvent ev) {
                            checkOut(remotefilename);
                        }
                    });
                } else {
                    item = new JMenuItem("Checkin");
                    p.add(item);
                    item.addActionListener(new ActionListener() {
                        public void actionPerformed(ActionEvent ev) {
                            checkIn(remotefilename);
                        }
                    });
                    item = new JMenuItem("UnCheckout");
                    p.add(item);
                    item.addActionListener(new ActionListener() {
                        public void actionPerformed(ActionEvent ev) {
                            uncheckout(remotefilename);
                        }
                    });
                }
                if((tree.getModel().isLeaf(tree.getSelectionPath()
                            .getLastPathComponent()))
                    && ((editable.indexOf(".tcl") != -1)
                        || (editable.indexOf(".py") != -1)
                        || (editable.indexOf(".java") != -1)
                        || (editable.indexOf(".pl") != -1))){
                    if(response.indexOf("checkout")==-1){
                        item = new JMenuItem("View");
                        p.add(item);
                        item.addActionListener(new ActionListener() {
                            public void actionPerformed(ActionEvent ev) {
                                editTC(editable,false);
                            }
                        });
                    } else {
                        item = new JMenuItem("Edit");
                        p.add(item);
                        item.addActionListener(new ActionListener() {
                            public void actionPerformed(ActionEvent ev) {
                                editTC(editable, true);
                            }
                        });
                        item = new JMenuItem("Edit with");
                        p.add(item);
                        item.addActionListener(new ActionListener() {
                            public void actionPerformed(ActionEvent evnt) {
                                editWith(editable,remotefilename,true);
                            }
                        });
                        item = new JMenuItem("Editors");
                        p.add(item);
                        item.addActionListener(new ActionListener() {
                            public void actionPerformed(ActionEvent evnt) {
                                try {
                                    new Editors(ev.getLocationOnScreen()).setVisible(true);
                                } catch (Exception e) {
                                    System.out
                                            .println("There was an error in opening editors"+
                                                     " configuration window, please check "+
                                                     "configuration file");
                                    e.printStackTrace();
                                }
                            }
                        });
                    }
                }
            }
        }
        try{p.show(tree, (int)ev.getX(),(int)ev.getY());}
        catch(Exception e){e.printStackTrace();}
    }
    
    public void uncheckout(String remotefilename){
            HashMap<String,String>hash = new HashMap<String,String>();
            hash.put("command","cleartool unco -rm \""+remotefilename+"\"");
            String response = RunnerRepository.window.mainpanel.getP5().sendCommand(hash,false);
            if(response.indexOf("Error")!=-1){
                String[] lines = response.split("\n");
                StringBuilder sb = new StringBuilder();
                sb.append("<html>");
                for(String l:lines){
                    sb.append(l);
                    sb.append("<br>");
                }
                sb.append("</html>");
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,tree,
                                      "ERROR", sb.toString());
            }
     }
    
    
     public void checkIn(String remotefilename){
         String comment = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
                                                    tree, "Comment", "Please enter comment");
         if(comment!=null){
             if(comment.equals("")){
                comment = " -nc ";
            } else {
                comment = " -c "+" \""+comment+"\" ";
            }
             HashMap<String,String>hash = new HashMap<String,String>();
             hash.put("command","cleartool ci " +comment+remotefilename);
             String response = RunnerRepository.window.mainpanel.getP5().sendCommand(hash,false);
             if(response.indexOf("Error")!=-1){
                String[] lines = response.split("\n");
                StringBuilder sb = new StringBuilder();
                sb.append("<html>");
                for(String l:lines){
                    sb.append(l);
                    sb.append("<br>");
                }
                sb.append("</html>");
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,tree, "ERROR", sb.toString());
            }
         }
     }
    
    
    public void checkOut(String remotefilename){
        String comment = CustomDialog.showInputDialog(JOptionPane.PLAIN_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
                                                    tree, "Comment", "Please enter comment");
        if(comment!=null){
            if(comment.equals("")){
                comment = " -nc ";
            } else {
                comment = " -c "+" \""+comment+"\" ";
            }
            HashMap<String,String>hash = new HashMap<String,String>();
            hash.put("command","cleartool co " +comment+remotefilename);
            String response = RunnerRepository.window.mainpanel.getP5().sendCommand(hash,false);
            if(response.indexOf("Error")!=-1){
                String[] lines = response.split("\n");
                StringBuilder sb = new StringBuilder();
                sb.append("<html>");
                for(String l:lines){
                    sb.append(l);
                    sb.append("<br>");
                }
                sb.append("</html>");
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,tree,
                                      "ERROR", sb.toString());
            }
            System.out.println("response: ---"+response+"---");
        }
    }

    /*
     * Propmpts user to select editor and 
     * opens selected editor for editing TC
     */
    public void editWith(String editable, String ctfile,boolean save) {
        try {
            JsonObject editors = RunnerRepository.getEditors();
            int length = editors.entrySet().size();
            Iterator iter = editors.entrySet().iterator();
            Entry entry;
            String[] vecresult;
            if (editors.get("DEFAULT") != null) {
                vecresult = new String[length - 1];
            } else {
                vecresult = new String[length];
            }
            int index = 0;
            for (int i = 0; i < length; i++) {
                entry = (Entry) iter.next();
                if (entry.getKey().toString().equals("DEFAULT")) {
                    continue;
                }
                vecresult[index] = entry.getKey().toString();
                index++;
            }
            JComboBox jComboBox1 = new JComboBox();
            JPanel p = getEditorsPanel(jComboBox1, vecresult);
            Object[] message = new Object[] { p };
            int r = (Integer) CustomDialog.showDialog(p,
                    JOptionPane.QUESTION_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
                    tree, "Please select an editor", null);
            if (r == JOptionPane.OK_OPTION) {
                String ID = jComboBox1.getSelectedItem().toString();
                String remotefilename = tree.getSelectionPath()
                        .getPathComponent(
                                tree.getSelectionPath().getPathCount() - 2)
                        + "/" + tree.getSelectionPath().getLastPathComponent();
                String localfilename = RunnerRepository.temp + RunnerRepository.getBar()
                        + "Twister" + RunnerRepository.getBar()
                        + tree.getSelectionPath().getLastPathComponent();
                if (ID.equals("Embedded")) {
                    openEmbeddedEditor(editable, remotefilename, localfilename,ctfile,save);
                } else {
                    
                    HashMap<String,String>hm = new HashMap<String,String>();
                    hm.put("command","get_test_file");
                    hm.put("file_name",remotefilename);
                    System.out.println("get_test_file: "+remotefilename);
                    String respons = RunnerRepository.window.mainpanel.getP5().sendCommand(hm,false);
//                     String respons = RunnerRepository.getRPCClient().execute("runPlugin", new Object[]{RunnerRepository.user,"ClearCase",hm}).toString();
                    System.out.println(respons);
                    File file2 = new File(localfilename);
                    
                    BufferedWriter writer = new BufferedWriter(new FileWriter(file2));
                    writer.write(respons);
                    writer.flush();
                    writer.close();
                    
                    
                    
//                     String result = RunnerRepository.getRPCClient().execute("getTestDescription", new Object[] { thefile }).toString();
//                     
//                     
//                     RunnerRepository.window.mainpanel.getP5().sendCommand("cp "+remotefilename+" ~");
//                     File file2 = copyFileLocaly(editable, localfilename);
//                     RunnerRepository.window.mainpanel.getP5().sendCommand("rm -f ~/"+editable);
//                     
//                     
//                     
                    String execute = RunnerRepository.getEditors().get(ID).getAsString();
                    executeCommand(execute,localfilename);
                    
                    FileReader reader = new FileReader(file2);
                    char[] c=new char[(int)file2.length()];
                    reader.read(c);
                    reader.close();
                    String content = new String(c);
                    System.out.println("---"+content+"---");
                    
                    hm = new HashMap<String,String>();
                    hm.put("command","set_test_file");
                    hm.put("file_name",remotefilename);
                    hm.put("content",content);
                    System.out.println("set_test_file: "+remotefilename);
                    String response = RunnerRepository.window.mainpanel.getP5().sendCommand(hm,false);
//                     String response = RunnerRepository.getRPCClient().execute("runPlugin", new Object[]{RunnerRepository.user,"ClearCase",hm}).toString();
                    System.out.println(response);
                    file2.delete();
//                     
//                     
//                     sendFileToServer(file2, editable, ctfile);
//                     
//                     
//                     
//                     
//                     file2.delete();
                }
            }
        } catch (Exception e) {
            System.out
                    .println("There was an error in opening editors "+
                             "window, please check configuration file");
            e.printStackTrace();
        }
    }

    /*
     * creates the editors panel
     */

    public JPanel getEditorsPanel(JComboBox jComboBox1, String[] vecresult) {
        JPanel p = new JPanel();
        JLabel jLabel1 = new JLabel();
        jLabel1.setText("Editor: ");
        jComboBox1.setModel(new DefaultComboBoxModel(vecresult));
        GroupLayout layout = new GroupLayout(p);
        p.setLayout(layout);
        layout.setHorizontalGroup(layout
                .createParallelGroup(GroupLayout.Alignment.LEADING)
                .addGroup(layout.createSequentialGroup()
                                .addContainerGap()
                                .addGroup(layout.createParallelGroup(
                                                GroupLayout.Alignment.LEADING)
                                                .addComponent(jLabel1))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                .addGroup(
                                        layout.createParallelGroup(
                                                GroupLayout.Alignment.LEADING)
                                                .addComponent(jComboBox1,
                                                            GroupLayout.PREFERRED_SIZE,
                                                            84,
                                                            GroupLayout.PREFERRED_SIZE))
                                .addContainerGap(GroupLayout.DEFAULT_SIZE,
                                                Short.MAX_VALUE)));
        layout.setVerticalGroup(layout
                .createParallelGroup(GroupLayout.Alignment.LEADING)
                .addGroup(
                        layout.createSequentialGroup()
                                .addContainerGap()
                                .addGroup(layout.createParallelGroup(
                                                GroupLayout.Alignment.BASELINE)
                                                .addComponent(jLabel1)
                                                .addComponent(jComboBox1,
                                                                GroupLayout.PREFERRED_SIZE,
                                                                GroupLayout.DEFAULT_SIZE,
                                                                GroupLayout.PREFERRED_SIZE))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.TRAILING))
                                .addContainerGap(GroupLayout.DEFAULT_SIZE,
                                                Short.MAX_VALUE)));
        return p;
    }

    /*
     * open default editor and edit selected TC
     */
    public void editTC(String editable, boolean save) {
        String defaulteditor;
        try {
            defaulteditor = RunnerRepository.getEditors().get("DEFAULT")
                    .getAsString();
        } catch (Exception e) {
            System.out.println("Default Editor not present, using embedded");
            defaulteditor = "Embedded";
        }
        String remotefilename = tree.getSelectionPath().getPathComponent(
                tree.getSelectionPath().getPathCount() - 2)
                + "/" + tree.getSelectionPath().getLastPathComponent();
        String localfilename = RunnerRepository.temp + RunnerRepository.getBar()
                + "Twister" + RunnerRepository.getBar()
                + tree.getSelectionPath().getLastPathComponent();
                
        String respons = new String(RunnerRepository.getRemoteFileContent(remotefilename, false,"TestConfigPath"));
//         HashMap<String,String>hm = new HashMap<String,String>();
//         hm.put("command","get_test_file");
//         hm.put("file_name",remotefilename);
//         
//         
//         System.out.println("get_test_file: "+remotefilename);
//         String respons = "";
//         try{respons = RunnerRepository.window.mainpanel.getP5().sendCommand(hm,false);}
// //             respons = RunnerRepository.getRPCClient().execute("runPlugin", new Object[]{RunnerRepository.user,"ClearCase",hm}).toString();}
//         catch(Exception e){
//             System.out.println("Could not get file content: "+remotefilename);
//             e.printStackTrace();
//         }
        System.out.println(respons);
        File file2 = new File(localfilename);
        
        try{BufferedWriter writer = new BufferedWriter(new FileWriter(file2));
            writer.write(respons);
            writer.flush();
            writer.close();
        }catch(Exception e){
            System.out.println("Could not write file: "+file2.getAbsolutePath()+" to local pc");
            e.printStackTrace();
        }
        
        
        
//                     String result = RunnerRepository.getRPCClient().execute("getTestDescription", new Object[] { thefile }).toString();
//                     
//                     
//                     RunnerRepository.window.mainpanel.getP5().sendCommand("cp "+remotefilename+" ~");
//                     File file2 = copyFileLocaly(editable, localfilename);
//                     RunnerRepository.window.mainpanel.getP5().sendCommand("rm -f ~/"+editable);
//                     
//                     
//                     
//         String execute = RunnerRepository.getEditors().get(ID).getAsString();
//         executeCommand(execute,localfilename);
//         
//         FileReader reader = new FileReader(file2);
//         char[] c=new char[(int)file2.length()];
//         reader.read(c);
//         reader.close();
//         String content = new String(c);
//         System.out.println("---"+content+"---");
//         
//         hm = new HashMap<String,String>();
//         hm.put("command","set_test_file");
//         hm.put("file_name",remotefilename);
//         hm.put("content",content);
//         String response = RunnerRepository.getRPCClient().execute("runPlugin", new Object[]{RunnerRepository.user,"ClearCase",hm}).toString();
//         System.out.println(response);
//         file2.delete();
                
//         RunnerRepository.window.mainpanel.getP5().sendCommand("cp "+remotefilename+" ~");
//         File file2 = copyFileLocaly(editable, localfilename);
//         RunnerRepository.window.mainpanel.getP5().sendCommand("rm -f ~/"+editable);
        
        if (defaulteditor.equals("Embedded")) {
            openEmbeddedEditor(editable, editable, localfilename, remotefilename,save);
        } else {
            executeCommand(RunnerRepository.getEditors().get(defaulteditor).toString(),localfilename);
            FileReader reader = null;
            try{reader = new FileReader(file2);}
            catch(Exception e){
                System.out.println("Could not get file: "+file2.getAbsolutePath());
                e.printStackTrace();
            }
            char[] c=new char[(int)file2.length()];
            try{reader.read(c);
                reader.close();}
            catch(Exception e){
                System.out.println("Could not read file: "+file2.getAbsolutePath());
                e.printStackTrace();
            }
            
            String content = new String(c);
            System.out.println("---"+content+"---");
            HashMap hm = new HashMap<String,String>();
            hm.put("command","set_test_file");
            hm.put("file_name",remotefilename);
            hm.put("content",content);
            System.out.println("set_test_file: "+remotefilename);
            String response = "";
            try{response = RunnerRepository.window.mainpanel.getP5().sendCommand(hm,false);}
//                 response = RunnerRepository.getRPCClient().execute("runPlugin", new Object[]{RunnerRepository.user,"ClearCase",hm}).toString();}
            catch(Exception e){
                System.out.println("Could not execute xmlrpc command");
                e.printStackTrace();
            }
            System.out.println(response);
            file2.delete();
        }
    }

    /*
     * refresh tree structure
     */
    public void refreshTree(final int X, final int Y) {
        new Thread() {
            public void run() {
                setEnabledTabs(false);
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
                setEnabledTabs(true);
            }
        }.start();
    }

    /*
     * executes the command for opening an editor
     */
    public void executeCommand(String command, String arg) {
        try {
            String line;
            command = command.replace("\\", "\\\\");
            arg = arg.replace("\\", "\\\\");
            System.out.println("Executing " + command + " command");
            Process p = Runtime.getRuntime().exec(new String[]{command,arg});
            p.waitFor();
            System.out.println(p.exitValue());
        } catch (Exception err) {
            System.out.println("Error in executing " + command + " command");
            err.printStackTrace();
        }
    }

    /*
     * opens a window for embeded editor
     */
    public void openEmbeddedEditor(String editable, final String remotefile,
                                    final String localfile, final String ctfile, boolean save) {
        final JFrame f = new JFrame();
        tree.setEnabled(false);
        RunnerRepository.window.mainpanel.p1.sc.g.setCanRequestFocus(false);
        f.setVisible(true);
        f.setBounds(200, 100, 500, 600);
        textarea = new JEditTextArea();
        f.setFocusTraversalKeysEnabled(false);
        textarea.setFocusTraversalKeysEnabled(false);
        JPopupMenu p = new JPopupMenu();
        JMenuItem item;
        item = new JMenuItem("Copy");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev) {
                textarea.copy();
            }
        });
        p.add(item);
        item = new JMenuItem("Cut");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev) {
                textarea.cut();
            }
        });
        p.add(item);
        item = new JMenuItem("Paste");
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ev) {
                textarea.paste();
            }
        });
        p.add(item);
        textarea.setRightClickPopup(p);
        textarea.getDocument().putProperty(PlainDocument.tabSizeAttribute, 4);
        if (editable.indexOf(".tcl") != -1) {
            textarea.setTokenMarker(new TCLTokenMarker());
        } else if (editable.indexOf(".py") != -1 || editable.indexOf(".java") != -1) {
            textarea.setTokenMarker(new PythonTokenMarker());
        } else if (editable.indexOf(".pl") != -1) {
            textarea.setTokenMarker(new PerlTokenMarker());
        }
        f.add(textarea);
        final File file = new File(localfile);
        JMenuBar menu = new JMenuBar();
        JMenu filemenu = new JMenu("File");
        if(save){
            JMenuItem saveuser = new JMenuItem("Save");
            saveuser.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent ev) {
                    try {
                        FileWriter filewriter = new FileWriter(file);
                        BufferedWriter out = new BufferedWriter(filewriter);
                        out.write(textarea.getText());
                        out.flush();
                        out.close();
                        filewriter.close();
//                         sendFileToServer(file, remotefile,ctfile);
                        FileReader reader = new FileReader(file);
                        char[] c=new char[(int)file.length()];
                        reader.read(c);
                        reader.close();
                        String content = new String(c);
                        System.out.println("---"+content+"---");
                        HashMap hm = new HashMap<String,String>();
                        hm.put("command","set_test_file");
                        hm.put("file_name",ctfile);
                        hm.put("content",content);
                        System.out.println("set_test_file: "+ctfile);
                        String response = RunnerRepository.window.mainpanel.getP5().sendCommand(hm,false);
//                         String response = RunnerRepository.getRPCClient().execute("runPlugin", new Object[]{RunnerRepository.user,"ClearCase",hm}).toString();
                        System.out.println(response);
                        file.delete();
                    } catch (Exception e) {
                        System.out.println("Could not save file : "
                                + localfile);
                    }
                }
            });
            filemenu.add(saveuser);
        }
        
        menu.add(filemenu);
        f.setJMenuBar(menu);
        BufferedReader bufferedReader = null;
        try {
            bufferedReader = new BufferedReader(new FileReader(localfile));
        } catch (Exception e) {
            e.printStackTrace();
        }
        String line = null;
        try {
            StringBuffer buf = new StringBuffer();
            while ((line = bufferedReader.readLine()) != null) {
                buf.append(line + "\n");
            }
            bufferedReader.close();
            textarea.setText(buf.toString());
            textarea.setCaretPosition(0);
        } catch (Exception e) {
            System.out.println("failed to read file localy");
            e.printStackTrace();
        }
        f.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent ev) {
                tree.setEnabled(true);
                RunnerRepository.window.mainpanel.p1.sc.g.setCanRequestFocus(true);
                if (file.delete()) {
                    System.out.println("File deleted successfully");
                }
                textarea.setText("");
                f.dispose();
            }
        });
    }

    public static File copyFileLocaly(String filename, String localfilename) {
//         InputStream in = null;
        try {
            filename ="~/"+filename;
            System.out.print("Getting " + filename + " ....");
//             in = connection.get(filename);
            
        } catch (Exception e) {
            System.out.println("Could not get :" + filename);
            e.printStackTrace();
        }
//         InputStreamReader inputStreamReader = new InputStreamReader(in);
//         BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
        BufferedWriter writer = null;
//         String line;
        File file2 = new File(localfilename);
        try {
            writer = new BufferedWriter(new FileWriter(file2));
//             while ((line = bufferedReader.readLine()) != null) {
//                 writer.write(line);
//                 writer.newLine();
//             }
            String content = new String(RunnerRepository.getRemoteFileContent(filename, false,null));
            writer.write(content);
            writer.flush();
//             bufferedReader.close();
            writer.close();
//             inputStreamReader.close();
//             in.close();
            System.out.println("successfull");
        } catch (Exception e) {
            System.out.println("failed");
            e.printStackTrace();
        }
        return file2;
    }
    
//     public static void sendFileToServer(File localfile, String remotefile, String ctfile) {
//         try {
//             remotefile = connection.getHome()+"/"+remotefile;
//             FileInputStream in = new FileInputStream(localfile);
//             connection.put(in, remotefile);
//             in.close();
//             HashMap hash = new HashMap<String,String>();
//             hash.put("command","cp "+remotefile+" "+ctfile);
//             RunnerRepository.window.mainpanel.getP5().sendCommand("cp "+remotefile+" "+ctfile);
//             
//         } catch (Exception e) {
//             e.printStackTrace();
//             System.out.println("There was a problem in saving file "
//                     + localfile.getName() + " on hdd and uploading it to "
//                     + remotefile);
//         }
//     }

    public void refreshStructure() {
        //try{root.remove(0);}
        //catch(Exception e){}
        if(root.getChildCount()>0)root.remove(0);
//         HashMap<String, String> hash = new HashMap<String, String>();
//         hash.put("command", "get_path_tree");
//         hash.put("path", RunnerRepository.window.mainpanel.getP5().root);
//         String result = "";
//         System.out.println("get_path_tree: "+RunnerRepository.window.mainpanel.getP5().root);
        try{
            HashMap hash = RunnerRepository.getServerTCStructure(true);
            getList(root, hash,hash.get("data").toString());
            ((DefaultTreeModel)tree.getModel()).reload();
//             result = RunnerRepository.window.mainpanel.getP5().sendCommand(hash,false);
            
//             result= RunnerRepository.getRPCClient().execute("runPlugin", new Object[]{RunnerRepository.user,
//                                                                      "ClearCase",hash}).toString();
//             System.out.println(result);
        }
        catch(Exception e){
            System.out.println("Could not get tree from CE");
            e.printStackTrace();
            return;
        }
//         JsonObject el = (JsonObject)new JsonParser().parse(result);
//         JsonElement vob = el.get(RunnerRepository.window.mainpanel.getP5().root);
//         DefaultMutableTreeNode child2 = new DefaultMutableTreeNode(RunnerRepository.window.mainpanel.getP5().root,true);
//         root.add(child2);
//         RunnerRepository.window.mainpanel.getP5().buildTree(child2,(JsonObject)vob);
//         ((DefaultTreeModel) tree.getModel()).reload();
        tree.expandRow(0);
        selected = null;
        setDragging(false);
    }
    
    /*
     * construct the list for folders representation in jtree
     */
    public void getList(DefaultMutableTreeNode node, HashMap hash, String curentdir) {
        try {
            System.out.println(curentdir);
            DefaultMutableTreeNode child = new DefaultMutableTreeNode(curentdir);
            node.add(child);
            Object [] children = (Object [])hash.get("children");
            if(children!=null&&children.length>0){
                for(Object subchild:children){
                    String name = ((HashMap)subchild).get("data").toString();
                    if(((HashMap)subchild).get("folder")!=null){//folder
                        getList(child, (HashMap)subchild ,curentdir+"/"+name);
                    } else {//file
                        child2 = new DefaultMutableTreeNode(name,false);
                        child.add(child2);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void setEnabledTabs(boolean enable) {
        int nr = RunnerRepository.window.mainpanel.getTabCount();
        for (int i = 1; i < nr; i++) {
            RunnerRepository.window.mainpanel.setEnabledAt(i, enable);
        }
    }

    public void setDragging(boolean drag) {
        dragging = drag;
    }

    public boolean getDragging() {
        return dragging;
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
class Compare implements Comparator {

    public int compare(Object emp1, Object emp2) {
        return ((TreePath) emp1)
                .getLastPathComponent()
                .toString()
                .compareToIgnoreCase(
                        ((TreePath) emp2).getLastPathComponent().toString());
    }
}