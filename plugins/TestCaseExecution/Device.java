// /*
// File: Device.java ; This file is part of Twister.
// Version: 2.001
// 
// Copyright (C) 2012-2013 , Luxoft
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
// import javax.swing.JPanel;
// import java.awt.Color;
// import java.awt.event.MouseMotionAdapter;
// import java.awt.event.MouseAdapter;
// import java.awt.event.MouseEvent;
// import java.awt.Point;
// import javax.swing.JLabel;
// import javax.swing.BorderFactory;
// import javax.swing.border.BevelBorder;
// import java.util.ArrayList;
// import javax.swing.JTextField;
// import javax.swing.JButton;
// import java.awt.event.ActionListener;
// import java.awt.event.ActionEvent;
// import java.awt.event.KeyAdapter;
// import java.awt.event.KeyEvent;
// import java.awt.Dimension;
// import javax.swing.tree.DefaultTreeModel;
// import javax.swing.tree.DefaultMutableTreeNode;
// 
// public class Device{
//     private int X,Y;
//     String name= "";
//     String description="";
//     String id="";
//     String vendor="";
//     String type="";
//     String family="";
//     String model="";
//     ArrayList <String[]> properties =  new ArrayList <String[]>();
//     ArrayList <DeviceModule> modules =  new ArrayList <DeviceModule>();
//     Device reference;
//     
//     public Device(){reference = this;}
//         
//     public void updateInfo(){
//         Dut dut = Repository.window.mainpanel.p4.getDut();
//         dut.additem.setEnabled(true);
//         dut.additem.setText("Add module");
//         dut.remitem.setEnabled(true);
//         dut.remitem.setText("Remove device");
//         dut.temp = reference;
//         dut.tname.setText(name.toString());
//         dut.ttype.setText(type.toString());
//         dut.tvendor.setText(vendor.toString());
//         dut.tmodel.setText(model.toString());
//         dut.tfamily.setText(family.toString());
//         dut.tid.setText(id.toString());        
//         dut.tdescription.setText(description.toString());
//         dut.propname.setText("");
//         dut.propvalue.setText("");
//         updatePropertys();}
//         
//     public void updatePropertys(){
//         Repository.window.mainpanel.p4.getDut().properties.removeAll();
//         if(Repository.window.mainpanel.p4.getDut().nodetemp1.
//         getChildAt(Repository.window.mainpanel.p4.getDut().nodetemp1.getChildCount()-1).isLeaf()){
//             while(Repository.window.mainpanel.p4.getDut().nodetemp1.getChildCount()>6){
//                 ((DefaultTreeModel)Repository.window.mainpanel.p4.getDut().explorer.tree.getModel()).
//                 removeNodeFromParent(((DefaultMutableTreeNode)Repository.window.
//                                         mainpanel.p4.getDut().nodetemp1.getChildAt(6)));}}
//         else{
//             while(Repository.window.mainpanel.p4.getDut().nodetemp1.getChildAt(6).isLeaf()){
//                 ((DefaultTreeModel)Repository.window.mainpanel.p4.getDut().explorer.tree.getModel()).
//                 removeNodeFromParent(((DefaultMutableTreeNode)Repository.window.mainpanel.p4.
//                                         getDut().nodetemp1.getChildAt(6)));}}
//         for(int i =0;i<properties.size();i++){
//             DefaultMutableTreeNode child2 = new DefaultMutableTreeNode(properties.get(i)[0]+" - "+
//                                                                         properties.get(i)[1],false);
//             if(Repository.window.mainpanel.p4.getDut().nodetemp1.
//             getChildAt(Repository.window.mainpanel.p4.getDut().nodetemp1.getChildCount()-1).isLeaf()){
//                 ((DefaultTreeModel)Repository.window.mainpanel.p4.getDut().explorer.tree.getModel()).
//                 insertNodeInto(child2,Repository.window.mainpanel.p4.getDut().nodetemp1,
//                                 Repository.window.mainpanel.p4.getDut().nodetemp1.getChildCount());}
//             else{
//                 ((DefaultTreeModel)Repository.window.mainpanel.p4.getDut().explorer.tree.getModel()).
//                 insertNodeInto(child2,Repository.window.mainpanel.p4.getDut().nodetemp1,6+i);}
//             final JButton b = new JButton("remove");
//             b.setBounds(280,i*23+18,78,19);
//             b.addActionListener(new ActionListener(){
//                 public void actionPerformed(ActionEvent ev){
//                     properties.remove(Repository.window.mainpanel.p4.getDut().
//                                         properties.getComponentZOrder(b)/3);
//                     updatePropertys();}});
//             Repository.window.mainpanel.p4.getDut().properties.add(b);
//             final JTextField text1 = new JTextField();
//             text1.setText(properties.get(i)[0]);
//             text1.setBounds(6,i*23+18,135,25);
//             text1.addKeyListener(new KeyAdapter(){
//                 public void keyReleased(KeyEvent ev){
//                     properties.get(Repository.window.mainpanel.p4.getDut().
//                                     properties.getComponentZOrder(text1)/3)[0]=text1.getText();
//                     ((DefaultMutableTreeNode)Repository.window.mainpanel.p4.getDut().nodetemp1.
//                     getChildAt(6+(Repository.window.mainpanel.p4.getDut().properties.getComponentZOrder(text1)/3))).
//                     setUserObject(text1.getText()+" - "+properties.get(Repository.window.mainpanel.p4.getDut().
//                                                                         properties.getComponentZOrder(text1)/3)[1]);
//                     ((DefaultTreeModel)Repository.window.mainpanel.p4.getDut().explorer.tree.getModel()).
//                     nodeChanged(Repository.window.mainpanel.p4.getDut().nodetemp1.
//                                 getChildAt(6+(Repository.window.mainpanel.p4.getDut().
//                                                 properties.getComponentZOrder(text1)/3)));}});
//             final JTextField text2 = new JTextField();
//             text2.setText(properties.get(i)[1]);
//             text2.setBounds(143,i*23+18,135,25);    
//             text2.addKeyListener(new KeyAdapter(){
//                 public void keyReleased(KeyEvent ev){
//                     properties.get(Repository.window.mainpanel.p4.getDut().
//                                     properties.getComponentZOrder(text1)/3)[1]=text2.getText();
//                     ((DefaultMutableTreeNode)Repository.window.mainpanel.p4.getDut().nodetemp1.
//                     getChildAt(6+(Repository.window.mainpanel.p4.getDut().properties.getComponentZOrder(text1)/3))).
//                     setUserObject(properties.get(Repository.window.mainpanel.p4.
//                                                 getDut().properties.getComponentZOrder(text1)/3)[0]+" - "+
//                                   text2.getText());
//                     ((DefaultTreeModel)Repository.window.mainpanel.p4.getDut().explorer.tree.getModel()).
//                     nodeChanged(Repository.window.mainpanel.p4.getDut().nodetemp1.
//                                 getChildAt(6+(Repository.window.mainpanel.p4.getDut().properties.
//                                                 getComponentZOrder(text1)/3)));}});
//             Repository.window.mainpanel.p4.getDut().properties.add(text2);
//             Repository.window.mainpanel.p4.getDut().properties.add(text1);}
//         Repository.window.mainpanel.p4.getDut().properties.setPreferredSize(
//             new Dimension(Repository.window.mainpanel.p4.getDut().properties.getWidth(),
//                             properties.size()*23+18));
//         Repository.window.mainpanel.p4.getDut().properties.revalidate();
//         Repository.window.mainpanel.p4.getDut().properties.repaint();}
//         
//     public void setDescription(String description){
//         this.description = description;}
//         
//     public void setID(String id){
//         this.id=id;}
//         
//     public void setVendor(String vendor){
//         this.vendor = vendor;}
//         
//     public void setType(String type){
//         this.type=type;}
//         
//     public String toString(){
//         return "Device: "+name.toString();}
//         
//     public void addModule(DeviceModule module){
//         modules.add(module);}
//         
//     public void setFamily(String family){
//         this.family=family;}
//     
//     public void setModel(String model){
//         this.model=model;}
//             
//     public void setName(String name){
//         this.name=name;}}
