/*
File: NodePanel.java ; This file is part of Twister.
Version: 2.001

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

public class NodePanel extends JPanel{
    private Node parent;
    private JTextField tname,tid,tpath;
    private JButton add;
    private DefaultMutableTreeNode treenode;
    private JTree tree;
    private JPanel proppanel;
    private XmlRpcClient client;
    private JList tep;

    public NodePanel(JTree tree,XmlRpcClient client){
        this.tree = tree;
        this.client = client;
        init();
    }
    
    public void setParent(Node parent,DefaultMutableTreeNode treenode){
        this.parent = parent;
        this.treenode = treenode;
        if(parent!=null&&treenode!=null){
            if(!add.isEnabled()){
                add.setEnabled(true);
            }
        } else{
            if(add.isEnabled()){
                add.setEnabled(false);
            }
        }
        initNewParent();
        updateProperties();
    }
    
    public Node getNodeParent(){
        return parent;
    }
    
    private void initNewParent(){
        if(parent!=null){
            tname.setEnabled(true);
            tname.setText(parent.getName());
            tid.setText(parent.getID());
            tpath.setText(parent.getPath().getPath());
            if(parent.getParent().getParent()==null){
                populateEPs();
                if(!tep.isEnabled()){
                    tep.setEnabled(true);
                }
            } else {
                tep.clearSelection();
                if(tep.isEnabled()){
                    tep.setEnabled(false);
                }
            }
        } else {
            tname.setText("");
            tid.setText("");
            tpath.setText("");
            tep.clearSelection();
            tep.setEnabled(false);
            tname.setEnabled(false);
        }
    }

    private void init(){
        JLabel name = new JLabel("Name: ");
        JLabel id = new JLabel("ID: ");
        JLabel ep = new JLabel("Run on EP: ");
        JLabel path = new JLabel("Path:");
        tep = new JList();
        tname = new JTextField();
        tep.setEnabled(false);
        tname.setEnabled(false);
        tid = new JTextField();
        tid.setEditable(false);
        tpath = new JTextField();
        tpath.setEditable(false);
        JPanel jPanel1 = new JPanel();
        JScrollPane jScrollPane2 = new JScrollPane();
        JScrollPane epscroll = new JScrollPane(tep);
        proppanel = new JPanel();

        add = new JButton("Add");
        add.setEnabled(false);


        setBorder(BorderFactory.createBevelBorder(BevelBorder.RAISED));
        jPanel1.setBorder(BorderFactory.createTitledBorder( "Properties"));

        jScrollPane2.setBorder(null);
        jScrollPane2.setPreferredSize(new Dimension(350, 150));

        proppanel.setPreferredSize(new Dimension(280, 150));
        proppanel.setLayout(null);

        proppanel.add(add);
        add.setBounds(310, 5, 90, 23);

        jScrollPane2.setViewportView(proppanel);

        GroupLayout jPanel1Layout = new GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane2, GroupLayout.PREFERRED_SIZE, 0, Short.MAX_VALUE)
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(jScrollPane2, GroupLayout.Alignment.TRAILING,
                          GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
        );
    
    GroupLayout optpanLayout = new GroupLayout(this);
    this.setLayout(optpanLayout);
    optpanLayout.setHorizontalGroup(
        optpanLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
        .addGroup(optpanLayout.createSequentialGroup()
            .addContainerGap()
            .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                .addGroup(optpanLayout.createSequentialGroup()
                    .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                        .addComponent(ep)
                        .addComponent(name)
                        .addComponent(id)
                        .addComponent(path))
                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                    .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.TRAILING, false)
                        .addComponent(epscroll, GroupLayout.Alignment.LEADING,
                                      GroupLayout.DEFAULT_SIZE, 151, Short.MAX_VALUE)
                        .addComponent(tid, GroupLayout.Alignment.LEADING, 
                                      GroupLayout.DEFAULT_SIZE, 151, Short.MAX_VALUE)
                        .addComponent(tname, GroupLayout.Alignment.LEADING)
                        .addComponent(tpath))
                    .addGap(0, 105, Short.MAX_VALUE))
                .addComponent(jPanel1, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
            .addContainerGap())
        );
        optpanLayout.setVerticalGroup(
            optpanLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(optpanLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(ep)
                    .addComponent(epscroll, 80, 80, 80))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                
                .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(name)
                    .addComponent(tname, GroupLayout.PREFERRED_SIZE, 
                                  GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                
                .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(id)
                    .addComponent(tid, GroupLayout.PREFERRED_SIZE, 
                                  GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                
                .addGroup(optpanLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(path)
                    .addComponent(tpath, GroupLayout.PREFERRED_SIZE, 
                                  GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(18, 18, 18)
                .addComponent(jPanel1, GroupLayout.DEFAULT_SIZE, 
                               GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );
        
        tname.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                try{
                    if(parent.getName().equals(tname.getText()))return;
                    if(!checkExistingName(parent, tname.getText())){
                        String query = client.execute("renameResource", new Object[]{parent.getID(),
                                                                                    tname.getText()}).toString();
                        if(query.equals("true")){
                            updatePaths(treenode, parent);
                            parent.setName(tname.getText());
                            tpath.setText(parent.getPath().getPath());
                            ((DefaultTreeModel)tree.getModel()).nodeChanged(treenode);
                            Repository.window.mainpanel.p1.suitaDetails.setComboTBs();
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
                            String path = parent.getParent().getID();                        
                            String query = "{'"+resp+"':''}";
                            query = client.execute("setResource", new Object[]{name,path,query}).toString();
                            if(query.equals("true")){
                                parent.addProperty(resp, "");
                                updateProperties();
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
        populateEPs();
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
    
    
    public void updateProperties(){
        proppanel.removeAll();
        if(parent!=null){
            int size = parent.getProperties().size();
        
            Object [] keys = parent.getProperties().keySet().toArray();
            Object [] values = parent.getProperties().values().toArray();
            
            for(int i=0;i<size;i++){
                
                final JLabel jLabel1 = new JLabel("Name: ");
                final MyTextField jTextField1 = new MyTextField(keys[i].toString());
                JLabel jLabel2 = new JLabel("Value:");
                final JTextField jTextField2 = new JTextField();
                
    
                proppanel.add(jLabel1);
                jLabel1.setBounds(5, i*30+5, 210, 14);
                proppanel.add(jTextField1);
                jTextField1.setBounds(50, i*30+5, 95, 20);
                
                jTextField1.addKeyListener(new KeyAdapter(){
                    public void keyReleased(KeyEvent ev){
                        try{
                            if(jTextField1.getText().equals(jTextField1.getOldValue())) return;
                            if(parent.getPropery(jTextField1.getText())==null){
                                String resp = client.execute("renameResource", new Object[]{parent.getID()+":"+jTextField1.getOldValue(),
                                                                            jTextField1.getText()}).toString();
                                if(resp.equals("true")){
		                            parent.addProperty(jTextField1.getText(), parent.getProperties().remove(jTextField1.getOldValue()).toString());                                    jTextField1.setOldValue(jTextField1.getText());
                                } else {
                                    jTextField1.setText(jTextField1.getOldValue());
                                }
                            } else {
                                jTextField1.setText(jTextField1.getOldValue());
                                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,NodePanel.this,
                                                      "Warning", "Property already exists!");
                            }
                        }catch(Exception e){e.printStackTrace();}
                    }
                });
                proppanel.add(jLabel2);
                jLabel2.setBounds(160, i*30+5, 45, 14);
                proppanel.add(jTextField2);
                jTextField2.setBounds(205, i*30+2, 100, 20);
                jTextField2.setText(values[i].toString());
                jTextField2.addKeyListener(new KeyAdapter(){
                    public void keyReleased(KeyEvent ev){
                        String key = jTextField1.getText();
                        String value = jTextField2.getText();
                        parent.addProperty(key,value);
                        String path = parent.getParent().getID();
                        String name = parent.getName();
                        String query = "{'"+key+"':'"+value+"'}";
                        try{String resp = client.execute("setResource", new Object[]{name,path,query}).toString();}
                        catch(Exception e){e.printStackTrace();}
                    }
                });
                
                JButton remove = new JButton("Remove");
                remove.setBounds(310, i*30+2, 90, 20);
                remove.addActionListener(new ActionListener(){
                    public void actionPerformed(ActionEvent ev){
                        try{
                            String s = client.execute("deleteResource", new Object[]{parent.getID()+":"+
                                                      jTextField1.getText()}).toString();
                            if(s.equals("true")){
                                parent.getProperties().remove(jTextField1.getText());
                                updateProperties();
                            }
                        } catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                });
                proppanel.add(jLabel1);
                proppanel.add(jLabel2);
                proppanel.add(jTextField2);
                proppanel.add(remove);
            }
            add.setBounds(310, (size*30)+2, 90, 23);
            proppanel.add(add);
            proppanel.setPreferredSize(new Dimension(280, (size*30)+30));
        }
        proppanel.repaint();
    }
    
    private boolean checkExistingName(Node node, String name){
        try{
            String [] path = node.getPath().getPath().split("/");
            path[path.length-1] = name;
            StringBuilder sb = new StringBuilder();
            for(String s:path){
                sb.append(s);
                sb.append("/");            
            }
            String s = client.execute("getResource", new Object[]{sb.toString()}).toString();
            if(s.equals("false")){
                return false;
            } else {
                return true;
            }
        } catch (Exception e){
            e.printStackTrace();
            return false;
        }
    }
    
    
    public void populateEPs(){
        try{
            StringBuilder b = new StringBuilder();
            String st;
            for(String s:Repository.getRemoteFileContent(Repository.REMOTEEPIDDIR).split("\n")){
                if(s.indexOf("[")!=-1){
                    st = s.substring(s.indexOf("[")+1, s.indexOf("]"));
                    if(st.toUpperCase().indexOf("PLUGIN")==-1){
                        b.append(s.substring(s.indexOf("[")+1, s.indexOf("]"))+";");
                    }
                }
            }
            String [] vecresult = b.toString().split(";");
//             String line = null;
//             InputStream in = Repository.c.get(Repository.REMOTEEPIDDIR);
//             InputStreamReader inputStreamReader = new InputStreamReader(in);
//             BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
//             StringBuilder b=new StringBuilder();
//             while ((line=bufferedReader.readLine())!= null){
//                 if(line.indexOf("[")!=-1){
//                     b.append(line.substring(line.indexOf("[")+1, line.indexOf("]"))+";");
//                 }
//             }
//             bufferedReader.close();
//             inputStreamReader.close();
//             in.close();
//             String result = b.toString();
//             String [] vecresult = result.split(";");
            for(ListSelectionListener l:tep.getListSelectionListeners()){
                tep.removeListSelectionListener(l);
            }
            tep.setModel(new DefaultComboBoxModel(vecresult));
            ArrayList<String> array = new ArrayList<String>(Arrays.asList(vecresult));
            if(parent!=null&&parent.getEPs()!=null){
                String [] strings = parent.getEPs().split(";");
                int [] sel = new int[strings.length];
                for(int i=0;i<strings.length;i++){
                    sel[i]=array.indexOf(strings[i]);
                }
                tep.setSelectedIndices(sel);
            }
            
            tep.addListSelectionListener(new MyListSelectionListener());
        } catch (Exception e){e.printStackTrace();}
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
                String path = parent.getParent().getID();
                String name = parent.getName();
                String query = "{'epnames':'"+sb.toString()+"'}";
                try{String resp = client.execute("setResource", new Object[]{name,path,query}).toString();
                    if(resp.equals("true")){
                        parent.setEPs(sb.toString());
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
