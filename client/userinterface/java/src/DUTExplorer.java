// /*
// File: DUTExplorer.java ; This file is part of Twister.
// 
// Copyright (C) 2012 , Luxoft
// 
// Authors: Andrei Costachi <acostachi@luxoft.com>
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
// http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// */
// import javax.swing.JTree;
// import javax.swing.tree.MutableTreeNode;
// import javax.swing.tree.DefaultTreeModel;
// import javax.swing.tree.DefaultMutableTreeNode;
// import javax.swing.tree.TreePath;
// import javax.swing.tree.TreeModel;
// import javax.swing.JPanel;
// import javax.swing.JScrollPane;
// import java.awt.Color;
// import java.awt.event.MouseEvent;
// import java.awt.event.MouseAdapter;
// import java.awt.event.ActionListener;
// import java.awt.event.ActionEvent;
// import javax.swing.JPopupMenu;
// import javax.swing.JMenuItem;
// import javax.swing.JTextField;
// import javax.swing.JOptionPane;
// import javax.swing.tree.TreeSelectionModel;
// import javax.swing.plaf.metal.MetalIconFactory;
// import javax.swing.tree.DefaultTreeCellRenderer;
// import javax.swing.JButton;
// import javax.swing.BoxLayout;
// import javax.swing.JLabel;
// import java.awt.BorderLayout;
// import com.twister.CustomDialog;
// 
// public class DUTExplorer extends JPanel{
//     JTree tree;
//     DefaultMutableTreeNode root;
//     
//     public DUTExplorer(){
//         setBounds(5,5,610,643);
//         setLayout(null);
//         setBackground(Color.RED);
//         root = new DefaultMutableTreeNode("root", true);
//         tree = new JTree(root);
//         tree.setCellRenderer(new CustomIconRenderer());
//         tree.expandRow(1);
//         tree.setDragEnabled(false);
//         tree.setRootVisible(false); 
//         tree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
//         ((DefaultTreeCellRenderer)(tree.getCellRenderer())).setLeafIcon(null);
//         JScrollPane scroll = new JScrollPane(tree);
//         scroll.setBounds(0,0,610,643);
//         add(scroll);
//         tree.addMouseListener(new MouseAdapter(){
//             public void mouseReleased(MouseEvent ev){
//                 TreePath tp = tree.getPathForLocation(ev.getX(), ev.getY());
//                 if (tp != null){
//                     if(ev.getButton() == MouseEvent.BUTTON3){                                          
//                         tree.clearSelection();
//                         if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Device){
//                             tree.addSelectionPath(tp);
//                             Repository.window.mainpanel.p4.getDut().nodetemp1 = (DefaultMutableTreeNode)tp.getLastPathComponent();
//                             refreshPopup((DefaultMutableTreeNode)tp.getLastPathComponent(),ev,2);}
//                         else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DeviceModule){
//                             tree.addSelectionPath(tp);
//                             Repository.window.mainpanel.p4.getDut().nodetemp2 = (DefaultMutableTreeNode)tp.getLastPathComponent();
//                             refreshPopup((DefaultMutableTreeNode)tp.getLastPathComponent(),ev,1);}
//                         else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DevicePort){
//                             tree.addSelectionPath(tp);
//                             Repository.window.mainpanel.p4.getDut().nodetemp3 = (DefaultMutableTreeNode)tp.getLastPathComponent();
//                             refreshPopup((DefaultMutableTreeNode)tp.getLastPathComponent(),ev,0);}
//                         else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof TestBed){
//                             tree.addSelectionPath(tp);
//                             Repository.window.mainpanel.p4.getDut().nodetemp0 = (DefaultMutableTreeNode)tp.getLastPathComponent();
//                             refreshPopup((DefaultMutableTreeNode)tp.getLastPathComponent(),ev,3);}
//                         else{Repository.window.mainpanel.p4.getDut().clearSelection();}}
//                     else if(ev.getButton() == MouseEvent.BUTTON1){
//                         if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Device){
//                             Repository.window.mainpanel.p4.getDut().nodetemp1 = (DefaultMutableTreeNode)tp.getLastPathComponent();
//                             if(Repository.window.mainpanel.p4.getDut().SettingsPanel.
//                             getComponentZOrder(Repository.window.mainpanel.p4.getDut().p2)==-1){
//                                 removeElements();
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.add(Repository.window.mainpanel.p4.getDut().p2);
//                                 Repository.window.mainpanel.p4.getDut().jScrollPane4.
//                                     setViewportView(Repository.window.mainpanel.p4.getDut().properties);
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.revalidate();
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.repaint();}
//                             ((Device)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject()).updateInfo();}
//                         else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DeviceModule){
//                             Repository.window.mainpanel.p4.getDut().nodetemp2 = (DefaultMutableTreeNode)tp.getLastPathComponent();
//                             if(Repository.window.mainpanel.p4.getDut().SettingsPanel.
//                             getComponentZOrder(Repository.window.mainpanel.p4.getDut().p3)==-1){
//                                 removeElements();
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.add(Repository.window.mainpanel.p4.getDut().p3);
//                                 Repository.window.mainpanel.p4.getDut().jScrollPane4.
//                                     setViewportView(Repository.window.mainpanel.p4.getDut().properties2);
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.revalidate();
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.repaint();}    
//                             ((DeviceModule)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject()).updateInfo();}
//                         else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof TestBed){
//                             Repository.window.mainpanel.p4.getDut().nodetemp0 = (DefaultMutableTreeNode)tp.getLastPathComponent();
//                             if(Repository.window.mainpanel.p4.getDut().SettingsPanel.
//                             getComponentZOrder(Repository.window.mainpanel.p4.getDut().p1)==-1){
//                                 removeElements();
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.add(Repository.window.mainpanel.p4.getDut().p1);
//                                 Repository.window.mainpanel.p4.getDut().jScrollPane4.setViewportView(null);
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.revalidate();
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.repaint();}    
//                             ((TestBed)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject()).updateInfo();}
//                         else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DevicePort){{
//                             Repository.window.mainpanel.p4.getDut().nodetemp3 = (DefaultMutableTreeNode)tp.getLastPathComponent();
//                             if(Repository.window.mainpanel.p4.getDut().SettingsPanel.
//                             getComponentZOrder(Repository.window.mainpanel.p4.getDut().p4)==-1){
//                                 removeElements();
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.add(Repository.window.mainpanel.p4.getDut().p4);
//                                 Repository.window.mainpanel.p4.getDut().jScrollPane4.
//                                     setViewportView(Repository.window.mainpanel.p4.getDut().properties3);
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.revalidate();
//                                 Repository.window.mainpanel.p4.getDut().SettingsPanel.repaint();}
//                             ((DevicePort)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject()).updateInfo();}}
//                         else{Repository.window.mainpanel.p4.getDut().clearSelection();}}}
//                 else{Repository.window.mainpanel.p4.getDut().clearSelection(); 
//                     tree.clearSelection();
//                     if(ev.getButton() == MouseEvent.BUTTON3){ 
//                         refreshPopup(null,ev,0);}}}});}
//                         
//     public void removeElements(){
//         Repository.window.mainpanel.p4.getDut().SettingsPanel.remove(Repository.window.mainpanel.p4.getDut().p1);
//         Repository.window.mainpanel.p4.getDut().SettingsPanel.remove(Repository.window.mainpanel.p4.getDut().p3);
//         Repository.window.mainpanel.p4.getDut().SettingsPanel.remove(Repository.window.mainpanel.p4.getDut().p4);
//         Repository.window.mainpanel.p4.getDut().jScrollPane4.remove(Repository.window.mainpanel.p4.getDut().properties2);
//         Repository.window.mainpanel.p4.getDut().jScrollPane4.remove(Repository.window.mainpanel.p4.getDut().properties3);
//         Repository.window.mainpanel.p4.getDut().SettingsPanel.remove(Repository.window.mainpanel.p4.getDut().p2);
//         Repository.window.mainpanel.p4.getDut().jScrollPane4.remove(Repository.window.mainpanel.p4.getDut().properties);}
//                 
//     public void refreshPopup(final DefaultMutableTreeNode element,MouseEvent ev,int type){
//         JPopupMenu p = new JPopupMenu();
//         JMenuItem item;
//         if(element == null){
//             item = new JMenuItem("Add TestBed");        
//             item.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     addTestBed();}});
//             p.add(item);}
//         else if(type == 3){
//             item = new JMenuItem("Add Device");        
//             item.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     addDevice(element);}});
//             p.add(item);
//             item = new JMenuItem("Remove TestBed");        
//             item.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     removeElement(element);}});
//             p.add(item);}
//         else if(type == 2){
//             item = new JMenuItem("Add Module");        
//             item.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     addModule(element);}});
//             p.add(item);
//             item = new JMenuItem("Remove Device");        
//             item.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     removeElement(element);}});
//             p.add(item);}
//         else if(type == 1){
//             item = new JMenuItem("Add Port");        
//             item.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     addPort(element);}});
//             p.add(item);
//             item = new JMenuItem("Remove module");        
//             item.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     removeElement(element);}});
//             p.add(item);}
//         else{item = new JMenuItem("Remove port");        
//             item.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     removeElement(element);}});
//             p.add(item);}
//         p.show(this.tree,ev.getX(),ev.getY());}
//   
      
//     public void removeElement(DefaultMutableTreeNode element){
//         ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(element);
//         Repository.window.mainpanel.p4.getDut().clearSelection();}
//         
//     public void addTestBed(){  
//         String user = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE, 
//                                                    JOptionPane.OK_CANCEL_OPTION, 
//                                                    DUTExplorer.this, "Name: ", 
//                                                    "Add testbed");
//         if(user!=null){
//             TestBed d = new TestBed();
//             d.setName(user);
//             DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
//             DefaultMutableTreeNode child2 = new DefaultMutableTreeNode("Id: "+d.id,false);
//             child.add(child2);
//             DefaultMutableTreeNode child3 = new DefaultMutableTreeNode("Description: "+d.description,false);
//             child.add(child3);
//             ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, root,root.getChildCount());
//             ((DefaultTreeModel)tree.getModel()).reload();}}
//     
//     public void addDevice(DefaultMutableTreeNode element){
//         String name = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
//                                                     DUTExplorer.this, "Name: ", "Add device");
//         if(name!=null){
//             Device d = new Device();
//             d.setName(name);
//             DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
//             DefaultMutableTreeNode child3 = new DefaultMutableTreeNode("Id: "+d.id,false);
//             child.add(child3);
//             DefaultMutableTreeNode child2 = new DefaultMutableTreeNode("Description: "+d.description,false);
//             child.add(child2);
//             DefaultMutableTreeNode child4 = new DefaultMutableTreeNode("Vendor: "+d.vendor,false);
//             child.add(child4);
//             DefaultMutableTreeNode child5 = new DefaultMutableTreeNode("Type: "+d.type,false);
//             child.add(child5);
//             DefaultMutableTreeNode child6 = new DefaultMutableTreeNode("Family: "+d.family,false);
//             child.add(child6);
//             DefaultMutableTreeNode child7 = new DefaultMutableTreeNode("Model: "+d.model,false);
//             child.add(child7);
//             ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, element,element.getChildCount());}}
//             
//     public void addModule(DefaultMutableTreeNode element){
//         String name = CustomDialog.showInputDialog(JOptionPane.QUESTION_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
//                                                     DUTExplorer.this, "Name: ", "Add module");
//         if(name!=null){
//             DeviceModule d = new DeviceModule(name);
//             DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
//             DefaultMutableTreeNode child3 = new DefaultMutableTreeNode("Module Type: "+d.name);
//             child.add(child3);
//             ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, element,element.getChildCount());}}
//             
//     public void addPort(DefaultMutableTreeNode element){
//         JTextField name = new JTextField("");
//         JTextField type = new JTextField("");
//         JPanel p = getPortPanel(name,type);
//         int r = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
//                                                                     DUTExplorer.this, "Add port",null);
//         if (r == JOptionPane.OK_OPTION){
//             DevicePort d = new DevicePort(name.getText(),type.getText());
//             DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
//             DefaultMutableTreeNode child3 = new DefaultMutableTreeNode("Port type: "+type.getText());
//             child.add(child3);
//             ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, element,element.getChildCount());}}
//         
//         
//     public JPanel getPortPanel(JTextField name,JTextField type){
//         JPanel p = new JPanel();
//         p.setLayout(new BoxLayout(p, BoxLayout.Y_AXIS));
//         JPanel jPanel1 = new JPanel();
//         JLabel jLabel3 = new JLabel();
//         JPanel jPanel2 = new JPanel();
//         JLabel jLabel4 = new JLabel();
//         jPanel1.setLayout(new java.awt.BorderLayout());
//         jLabel3.setText("Name: ");
//         jPanel1.add(jLabel3, BorderLayout.CENTER);
//         p.add(jPanel1);
//         p.add(name);
//         jPanel2.setLayout(new BorderLayout());
//         jLabel4.setText("Value: ");
//         jPanel2.add(jLabel4, BorderLayout.CENTER);
//         p.add(jPanel2);
//         p.add(type);
//         return p;}}