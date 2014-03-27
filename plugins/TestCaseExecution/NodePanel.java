/*
File: NodePanel.java ; This file is part of Twister.
Version: 2.009

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
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JButton;
import javax.swing.JScrollPane;
import javax.swing.BorderFactory;
import javax.swing.border.BevelBorder;
import java.awt.Color;
import java.awt.Dimension;
import javax.swing.GroupLayout;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JTree;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.DefaultMutableTreeNode;
import com.twister.CustomDialog;
import javax.swing.JOptionPane;
import org.apache.xmlrpc.client.XmlRpcClient;
import javax.swing.JList;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import javax.swing.event.ListSelectionListener;
import javax.swing.event.ListSelectionEvent;
import javax.swing.DefaultComboBoxModel;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Enumeration;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;

public class NodePanel extends JPanel{
    private Node parent;
    public JTextField tname;
    private JTextField tid,tpath;
    private JButton add;
    private DefaultMutableTreeNode treenode;
    private JTree tree;
    private JPanel proppanel;
    private XmlRpcClient client;

    public NodePanel(JTree tree,XmlRpcClient client){
        this.tree = tree;
        this.client = client;
        init();
    }
    
    public void setParent(Node parent,DefaultMutableTreeNode treenode,boolean editable){
        this.parent = parent;
        this.treenode = treenode;
        add.setEnabled(editable);
        initNewParent(editable);
        updateProperties(editable);
    }
    
    public Node getNodeParent(){
        return parent;
    }
    
    private void initNewParent(boolean editable){
        tname.setEnabled(editable);
        if(parent!=null){
            tname.setText(parent.getName());
            tid.setText(parent.getID());
            tpath.setText(parent.getPath().getPath());
        } else {
            tname.setText("");
            tid.setText("");
            tpath.setText("");
        }
    }

    private void init(){
        JLabel name = new JLabel("Name: ");
        JLabel id = new JLabel("ID: ");
        JLabel path = new JLabel("Path:");
        final JButton update = new JButton("Update");
        update.setEnabled(false);
        tname = new JTextField();
        tname.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                update.setEnabled(true);
            }
        });
        tname.setEnabled(false);
        tid = new JTextField();
        tid.setEditable(false);
        tpath = new JTextField();
        tpath.setEditable(false);
        JPanel jPanel1 = new JPanel();
        JScrollPane jScrollPane2 = new JScrollPane();
        proppanel = new JPanel();
        add = new JButton("Add");
        add.setEnabled(false);
        setBorder(BorderFactory.createBevelBorder(BevelBorder.RAISED));
        jPanel1.setBorder(BorderFactory.createTitledBorder( "Properties"));
        jScrollPane2.setBorder(null);
        jScrollPane2.setPreferredSize(new Dimension(350, 150));
        proppanel.setPreferredSize(new Dimension(280, 150));
        proppanel.setLayout(null);        
        add.setBounds(410, 5, 90, 23);
        jScrollPane2.setViewportView(proppanel);        
        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane2, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, 366, Short.MAX_VALUE)
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane2, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
        );
        GroupLayout optpanLayout = new GroupLayout(this);
        this.setLayout(optpanLayout);
        optpanLayout.setHorizontalGroup(
            optpanLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(optpanLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(optpanLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(optpanLayout.createSequentialGroup()
                        .addGroup(optpanLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(path)
                            .addComponent(name)
                            .addComponent(id))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(optpanLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(tid)
                            .addComponent(tpath)
                            .addGroup(optpanLayout.createSequentialGroup()
                                .addComponent(tname, javax.swing.GroupLayout.PREFERRED_SIZE, 313, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(update, javax.swing.GroupLayout.DEFAULT_SIZE, 85, Short.MAX_VALUE))))
                    .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap())
        );
        optpanLayout.setVerticalGroup(
            optpanLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(optpanLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(optpanLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(name)
                    .addComponent(tname, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(update))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(optpanLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(id)
                    .addComponent(tid, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(optpanLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(tpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(path))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );

        optpanLayout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {id, name, path, tid, tname, tpath, update});
        
        update.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                 try{
                    if(tname.getText().equals(""))return;
                    if(parent.getName().equals(tname.getText()))return;
                    if(!checkExistingName(parent, tname.getText())){
                        String query = client.execute("renameResource", new Object[]{parent.getID(),
                                                                                    tname.getText()}).toString();
                        if(query.equals("true")){
                            updatePaths(treenode, parent);
                            parent.setName(tname.getText());
                            tpath.setText(parent.getPath().getPath());
                            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                            RunnerRepository.window.mainpanel.p4.getTB().setSavedState(treenode,false);
                            update.setEnabled(false);
                        } else {
                            System.out.println("There was an error: "+query);
                            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,NodePanel.this,
                                                  "Warning", query);
                        }
                    } else {
                        tname.setText(parent.getName());
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,NodePanel.this,
                                              "Warning", "Name already exists!");
                    }
                }
                catch(Exception e){
                    e.printStackTrace();
                }
            }
        });
        
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                String resp = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE,
                                                    JOptionPane.OK_CANCEL_OPTION, 
                                                    NodePanel.this, "Property name", "Name: ");
                if(resp!=null&&!resp.equals("")){
                    try{
                        if(parent.getPropery(resp)==null){
                            String name = parent.getName();
                            String path = "";
                            if(parent.getParent()!=null){
                                path = parent.getParent().getID();                        
                            } else {
                                path = "/";
                            }
                            String query = "{'"+resp+"':''}";
                            query = client.execute("setResource", new Object[]{name,path,query}).toString();
                            if(query.equals("true")){
                                parent.addProperty(resp, "");
                                updateProperties(true);
                                RunnerRepository.window.mainpanel.p4.getTB().setSavedState(treenode,false);
                            }
                        } else {
                            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,NodePanel.this,
                                                  "Warning", "Property already exists!");
                        }
                    }
                    catch(Exception e){e.printStackTrace();}
                }
            }
        });
    }
    
    /*
     * method used to update path name in Test Beds configuration 
     * panel. It recursively updates tnode children paths
     */
    private void updatePaths(DefaultMutableTreeNode tnode, Node node){
        try{
            HashMap hash= (HashMap)client.execute("getResource", new Object[]{node.getID()});
            String path = hash.get("path").toString();
            node.setPath(path);
            Enumeration e = tnode.children();
            while(e.hasMoreElements()){
                DefaultMutableTreeNode o = (DefaultMutableTreeNode)e.nextElement();
                if(!o.isLeaf()){
                    updatePaths(o, (Node)o.getUserObject());
                }
            }
            ((DefaultTreeModel)tree.getModel()).nodeChanged(tnode.getChildAt(1));
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    
    
    public void updateProperties(boolean editable){
        proppanel.removeAll();
        if(parent!=null){
            int size = parent.getProperties().size();
            Object [] keys = parent.getProperties().keySet().toArray();
            Object [] values = parent.getProperties().values().toArray();
            for(int i=0;i<size;i++){
                final JButton update = new JButton("Update");
                update.setEnabled(false);
                final JLabel jLabel1 = new JLabel("Name: ");
                final MyTextField jTextField1 = new MyTextField(keys[i].toString());
                jTextField1.addKeyListener(new KeyAdapter(){
                    public void keyReleased(KeyEvent ev){
                        update.setEnabled(true);
                    }
                });
                jTextField1.setEnabled(editable);
                JLabel jLabel2 = new JLabel("Value:");
                final JTextField jTextField2 = new JTextField();
                jTextField2.addKeyListener(new KeyAdapter(){
                    public void keyReleased(KeyEvent ev){
                        update.setEnabled(true);
                    }
                });
                jTextField2.setEnabled(editable);
                proppanel.add(jLabel1);
                jLabel1.setBounds(5, i*30+5, 210, 14);
                proppanel.add(jTextField1);
                jTextField1.setBounds(50, i*30+5, 95, 20);
                proppanel.add(jLabel2);
                jLabel2.setBounds(160, i*30+5, 45, 14);
                proppanel.add(jTextField2);
                jTextField2.setBounds(205, i*30+2, 100, 20);
                jTextField2.setText(values[i].toString());
                update.setBounds(310, i*30+2, 90, 20);
                update.addActionListener(new ActionListener(){
                    public void actionPerformed(ActionEvent ev){
                        //update name
                        try{
                            if(!jTextField1.getOldValue().equals(jTextField1.getText())){
                                if(parent.getPropery(jTextField1.getText())==null){
                                    String resp = client.execute("renameResource", new Object[]{"/"+parent.getName()+":"+jTextField1.getOldValue(),
                                                                                                jTextField1.getText()}).toString();
                                    if(resp.equals("true")){
                                        parent.addProperty(jTextField1.getText(), parent.getProperties().remove(jTextField1.getOldValue()).toString());
                                        jTextField1.setOldValue(jTextField1.getText());
                                        RunnerRepository.window.mainpanel.p4.getTB().setSavedState(treenode,false);
                                        update.setEnabled(false);
                                    } else {
                                        jTextField1.setText(jTextField1.getOldValue());
                                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,NodePanel.this,"ERROR", resp);
                                    }
                                } else {
                                    CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,NodePanel.this,"Warning", "Property already exists!");
                                    jTextField1.setText(jTextField1.getOldValue());
                                }
                            }
                            
                        }catch(Exception e){e.printStackTrace();}
                        //update value
                        String key = jTextField1.getText();
                        String value = jTextField2.getText();
                        String path = "";
                        if(parent.getParent()!=null){
                            path = "/"+parent.getParent().getName();                        
                        } else {
                            path = "/";
                        }
                        String name = "/"+parent.getName();
                        String query = "{'"+key+"':'"+value+"'}";
                        try{String resp = client.execute("setResource", new Object[]{name,path,query}).toString();
                            if(resp.equals("true")){
                                parent.addProperty(key,value);
                                RunnerRepository.window.mainpanel.p4.getTB().setSavedState(treenode,false);
                                update.setEnabled(false);
                            }else{
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,NodePanel.this,"ERROR", resp);
                            }
                        }
                        catch(Exception e){e.printStackTrace();}
                    }});
                if(editable)proppanel.add(update);
                JButton remove = new JButton("Remove");
                remove.setBounds(410, i*30+2, 90, 20);
                remove.addActionListener(new ActionListener(){
                    public void actionPerformed(ActionEvent ev){
                        try{
                            if(jTextField1.getText().equals(""))return;
                            String s = client.execute("deleteResource", new Object[]{parent.getID()+":"+
                                                                    jTextField1.getText()}).toString();
                            if(s.equals("true")){
                                parent.getProperties().remove(jTextField1.getText());
                                System.out.println(parent.getProperties().toString());
                                updateProperties(true);
                                RunnerRepository.window.mainpanel.p4.getTB().setSavedState(treenode,false);
                            }
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                });
                proppanel.add(jLabel1);
                proppanel.add(jLabel2);
                proppanel.add(jTextField2);
                if(editable)proppanel.add(remove);
            }
            add.setBounds(410, (size*30)+2, 90, 23);
            if(editable)proppanel.add(add);
            proppanel.setPreferredSize(new Dimension(480, (size*30)+30));
        }
        proppanel.repaint();
    }
    
    private boolean checkExistingName(Node node, String name){
        try{
            String [] path = node.getPath().getPath().split("/");
            path[path.length-1] = name;
            StringBuilder sb = new StringBuilder();
            sb.append("/");
            for(String s:path){
                sb.append(s);
                sb.append("/");            
            }
            sb.setLength(sb.length()-1);
            String s = client.execute("getResource", new Object[]{sb.toString()}).toString();
            if(s.equalsIgnoreCase("false")||s.indexOf("*ERROR*")!=-1){
                return false;
            } else {
                return true;
            }
        } catch (Exception e){
            e.printStackTrace();
            return false;
        }
    }
    
    
    class MyListSelectionListener implements ListSelectionListener {
        public void valueChanged(ListSelectionEvent evt) {
            if (!evt.getValueIsAdjusting()&&parent!=null) {
                JList list = (JList)evt.getSource();
                StringBuilder sb = new StringBuilder();
                for(int i=0;i<list.getSelectedValuesList().size();i++){
                    sb.append(list.getSelectedValuesList().get(i).toString());
                    sb.append(";");
                }
                String path = "";
                if(parent.getParent()!=null){
                    path = parent.getParent().getID();                        
                } else {
                    path = "/";
                }
                String name = parent.getName();
                String query = "{'epnames':'"+sb.toString()+"'}";
                try{String resp = client.execute("setResource", new Object[]{name,path,query}).toString();
                    if(resp.equals("true")){
                        parent.setEPs(sb.toString());
                        RunnerRepository.window.mainpanel.p4.getTB().setSavedState(treenode,false);
                    }
                }
                catch(Exception e){e.printStackTrace();}
            }
        }
    } 
}
class MyTextField extends JTextField{
    private String oldValue;
    
    public MyTextField(String oldValue){
        super(oldValue);
        this.oldValue = oldValue;
    }
    
    public String getOldValue(){
        return oldValue;
    }
    
    public void setOldValue(String oldValue){
        this.oldValue = oldValue;
    }
}
