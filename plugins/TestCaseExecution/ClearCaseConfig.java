/*
File: ClearCaseConfig.java ; This file is part of Twister.
Version: 2.006

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

// import javax.swing.JPanel;
// import java.awt.Color;
// import javax.swing.GroupLayout;
// import javax.swing.BorderFactory;
// import javax.swing.SwingConstants;
// import javax.swing.JLabel;
// import javax.swing.LayoutStyle;
// import org.w3c.dom.Element;
// import org.w3c.dom.Document;
// import org.w3c.dom.NodeList;
// import org.w3c.dom.Node;
// import javax.swing.JOptionPane;
// import com.twister.CustomDialog;
// import javax.xml.parsers.DocumentBuilderFactory;
// import javax.xml.parsers.DocumentBuilder;
// import javax.xml.transform.TransformerFactory;
// import javax.xml.transform.Transformer;
// import javax.xml.transform.OutputKeys;
// import javax.xml.transform.dom.DOMSource;
// import java.io.File;
// import java.io.FileInputStream;
// import javax.xml.transform.Result;
// import javax.xml.transform.stream.StreamResult;
// import javax.xml.parsers.ParserConfigurationException;
// import javax.xml.transform.TransformerConfigurationException;
// import javax.swing.JCheckBox;
// import javax.swing.JTextField;
// import java.io.BufferedWriter;
// import java.io.FileWriter;
// import java.awt.event.ActionListener;
// import java.awt.event.ActionEvent;
// import javax.swing.JScrollPane;
// import java.util.ArrayList;
// import javax.swing.JButton;
// import java.awt.event.ItemListener;
// import java.awt.event.ItemEvent;
// import java.util.HashMap;
// import javax.swing.JList;
// import javax.swing.DefaultComboBoxModel;
// import javax.swing.JComboBox;
// import java.awt.Component;
// 
// 
// public class ClearCaseConfig extends JPanel{
//     private JPanel main;
//     private JLabel jLabel,jLabel1,jLabel10,jLabel11,jLabel12,
//                    jLabel13,jLabel14,jLabel15,jLabel2,
//                    jLabel3,jLabel4,jLabel5,jLabel6,jLabel7,
//                    jLabel8,jLabel9,jLabel16,jPanel5,jLabel17,
//                    jLabel18,jLabel19,jLabel20,jLabel21;
//     private JPanel jPanel1,jPanel2,jPanel3,
//                    jPanel4,jPanel6,jPanel7;
//     private JButton libbtn,predefbtn,usrsutbtn,cfgbtn,
//                     tcbtn,save,projbtn,tcbtn1,projbtn1,predefbtn1,
//                     libbtn1,cfgbtn1,usrsutbtn1;
//     private JTextField libpath,predefpath,predefview,
//                        tcpath,tcview,cfgview,cfgpath,projpath,
//                        usrsutpath,usrsutview,libview,projview,tcactivity,projactivity,
//                        libactivity,predefactivity,cfgactivity,usractivity;
//     private JCheckBox tcactive,predefactive,projactive,libactive,usrsutactive,cfgactive;
//     private JComboBox type;
//     public ArrayList change;//array to hold items that change based on type
//     private ClearCase cc;
//     
//     public ClearCaseConfig(Object[] addtochange, ClearCase cc){
//         this.cc = cc;
//         initComponents(addtochange);
//         interpretConfig((Element)getRemoteConfigContent().getFirstChild());
//     }
//     
//     
//     private void initComponents(Object[] addtochange) { 
//         tcbtn1 = new JButton();
//         projbtn1 = new JButton();
//         predefbtn1 = new JButton();
//         libbtn1 = new JButton();
//         cfgbtn1 = new JButton();
//         usrsutbtn1 = new JButton();
//         main = new JPanel();
//         add(main);
//         jPanel1 = new JPanel();
//         jLabel1 = new JLabel();
//         jLabel21 = new JLabel();
//         jLabel2 = new JLabel();
//         jPanel5 = new JLabel();
//         jLabel18 = new JLabel();
//         jLabel19 = new JLabel();
//         jLabel20 = new JLabel();
//         projpath = new JTextField();
//         tcactivity = new JTextField();
//         predefactivity = new JTextField();
//         projactivity = new JTextField();
//         cfgactivity = new JTextField();
//         libactivity = new JTextField();
//         projview = new JTextField();
//         usractivity = new JTextField();
//         projactive = new JCheckBox();
//         projbtn = new JButton();
//         jLabel3 = new JLabel();
//         type = new JComboBox();
//         jPanel3 = new JPanel();
//         jLabel6 = new JLabel();
//         jLabel7 = new JLabel();
//         jLabel17 = new JLabel();
//         predefpath = new JTextField();
//         predefview = new JTextField();
//         predefactive = new JCheckBox();
//         predefbtn = new JButton();
//         jPanel2 = new JPanel();
//         jLabel4 = new JLabel();
//         jLabel5 = new JLabel();
//         libpath = new JTextField();
//         libview = new JTextField();
//         libactive = new JCheckBox();
//         libbtn = new JButton();
//         jPanel4 = new JPanel();
//         jLabel8 = new JLabel();
//         jLabel9 = new JLabel();
//         tcpath = new JTextField();
//         tcview = new JTextField();
//         tcactive = new JCheckBox();
//         tcbtn = new JButton();
//         jLabel10 = new JLabel();
//         jLabel11 = new JLabel();
//         jPanel6 = new JPanel();
//         jLabel12 = new JLabel();
//         jLabel13 = new JLabel();
//         cfgpath = new JTextField();
//         cfgview = new JTextField();
//         cfgactive = new JCheckBox();
//         cfgbtn = new JButton();
//         jPanel7 = new JPanel();
//         jLabel14 = new JLabel();
//         jLabel15 = new JLabel();
//         jLabel16 = new JLabel();
//         usrsutpath = new JTextField();
//         usrsutview = new JTextField();
//         usrsutactive = new JCheckBox();
//         usrsutbtn = new JButton();
//         save = new JButton();
//         change = new ArrayList();
//         for(Object ob:addtochange){
//             change.add(ob);
//         }
//         jPanel1.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Projects Path"));
// 
//         jLabel1.setText("Path:");
// 
//         jLabel2.setText("View:");
//         projactive.setText("Active:         ");
//         projactive.setAlignmentY(0.0F);
//         projactive.setBorder(null);
//         projactive.setHorizontalTextPosition(SwingConstants.LEFT);
// 
//         projbtn1.setText("List Activities");
//         projbtn.setText("List Views");
//         projbtn.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listViews(projview);
//             }
//         });
//         projbtn1.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listActivities(projview.getText(),projactivity);
//             }
//         });
//         GroupLayout jPanel1Layout = new GroupLayout(jPanel1);
//         jPanel1.setLayout(jPanel1Layout);
//         jPanel1Layout.setHorizontalGroup(
//             jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel1Layout.createSequentialGroup()
//                 .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                     .addGroup(jPanel1Layout.createSequentialGroup()
//                         .addGap(10, 10, 10)
//                         .addComponent(projactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
//                         .addGap(0, 0, Short.MAX_VALUE))
//                     .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
//                         .addContainerGap()
//                         .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addComponent(jLabel1)
//                             .addComponent(jLabel2)
//                             .addComponent(jLabel17))
//                         .addGap(18, 18, 18)
//                         .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
//                                 .addComponent(projview)
//                                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                                 .addComponent(projbtn, javax.swing.GroupLayout.PREFERRED_SIZE, 90, javax.swing.GroupLayout.PREFERRED_SIZE))
//                             .addGroup(jPanel1Layout.createSequentialGroup()
//                                 .addComponent(projactivity)
//                                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                                 .addComponent(projbtn1))
//                             .addComponent(projpath))))
//                 .addContainerGap())
//         );
//         jPanel1Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {projbtn, projbtn1});
//         
//         jPanel1Layout.setVerticalGroup(
//             jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel1Layout.createSequentialGroup()
//                 .addGap(10, 10, 10)
//                 .addComponent(projactive)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel1)
//                     .addComponent(projpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel2)
//                     .addComponent(projview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(projbtn))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel17)
//                     .addComponent(projactivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(projbtn1))
//                 .addContainerGap(12, Short.MAX_VALUE))
//         );
// 
//         jPanel1Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {jLabel1, jLabel2, projactive, projactivity, projbtn, projbtn1, projpath, projview});
// 
//         jLabel3.setText("Type:");
// 
//         type.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Base", "UCM" }));
// 
//         jPanel3.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Predefined Suites Path"));
// 
//         jLabel6.setText("Path:");
// 
//         jLabel7.setText("View:");
//         predefactive.setText("Active:         ");
//         predefactive.setAlignmentY(0.0F);
//         predefactive.setBorder(null);
//         predefactive.setHorizontalTextPosition(SwingConstants.LEFT);
// 
//         predefbtn.setText("List Views");
//         predefbtn1.setText("List Activities");
//         predefbtn.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listViews(predefview);
//             }
//         });
//         predefbtn1.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listActivities(predefview.getText(),predefactivity);
//             }
//         });
//         GroupLayout jPanel3Layout = new GroupLayout(jPanel3);
//         jPanel3.setLayout(jPanel3Layout);
//         jPanel3Layout.setHorizontalGroup(
//             jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel3Layout.createSequentialGroup()
//                 .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                     .addGroup(jPanel3Layout.createSequentialGroup()
//                         .addGap(10, 10, 10)
//                         .addComponent(predefactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
//                         .addGap(0, 0, Short.MAX_VALUE))
//                     .addGroup(jPanel3Layout.createSequentialGroup()
//                         .addContainerGap()
//                         .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addComponent(jLabel18)
//                             .addComponent(jLabel7)
//                             .addComponent(jLabel6))
//                         .addGap(18, 18, 18)
//                         .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addComponent(predefpath)
//                             .addGroup(jPanel3Layout.createSequentialGroup()
//                                 .addComponent(predefview)
//                                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                                 .addComponent(predefbtn))
//                             .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel3Layout.createSequentialGroup()
//                                 .addComponent(predefactivity)
//                                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                                 .addComponent(predefbtn1)))))
//                 .addContainerGap())
//         );
//         
//         jPanel3Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {predefbtn, predefbtn1});
//         
//         jPanel3Layout.setVerticalGroup(
//             jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel3Layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addComponent(predefactive)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
//                 .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel6)
//                     .addComponent(predefpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel7)
//                     .addComponent(predefview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(predefbtn))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel18)
//                     .addComponent(predefactivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(predefbtn1))
//                 .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
//         );
// 
//         
//         jPanel3Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {jLabel6, jLabel7, predefactive, predefactivity, predefbtn, predefbtn1, predefpath, predefview});
//         
//         jPanel2.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Library Path"));
//         
//         jLabel4.setText("Path:");
// 
//         jLabel5.setText("View:");
//         libactive.setText("Active:         ");
//         libactive.setAlignmentY(0.0F);
//         libactive.setBorder(null);
//         libactive.setHorizontalTextPosition(SwingConstants.LEFT);
// 
//         libbtn.setText("List Views");
//         libbtn1.setText("List Activities");
//         libbtn.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listViews(libview);
//             }
//         });
//         libbtn1.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listActivities(libview.getText(),libactivity);
//             }
//         });
//         GroupLayout jPanel2Layout = new GroupLayout(jPanel2);
//         jPanel2.setLayout(jPanel2Layout);
//         jPanel2Layout.setHorizontalGroup(
//             jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel2Layout.createSequentialGroup()
//                 .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                     .addGroup(jPanel2Layout.createSequentialGroup()
//                         .addGap(10, 10, 10)
//                         .addComponent(libactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
//                         .addGap(0, 0, Short.MAX_VALUE))
//                     .addGroup(jPanel2Layout.createSequentialGroup()
//                         .addContainerGap()
//                         .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addComponent(jLabel5)
//                             .addComponent(jLabel19)
//                             .addComponent(jLabel4))
//                         .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
//                         .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel2Layout.createSequentialGroup()
//                                 .addComponent(libview)
//                                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                                 .addComponent(libbtn))
//                             .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel2Layout.createSequentialGroup()
//                                 .addComponent(libactivity)
//                                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                                 .addComponent(libbtn1))
//                             .addComponent(libpath))))
//                 .addContainerGap())
//         );
//         
//         jPanel2Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {libbtn, libbtn1});
// 
//         
//         jPanel2Layout.setVerticalGroup(
//             jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel2Layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addComponent(libactive)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel4)
//                     .addComponent(libpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel5)
//                     .addComponent(libview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(libbtn))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel19)
//                     .addComponent(libactivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(libbtn1))
//                 .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
//         );
// 
//         jPanel2Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {jLabel4, jLabel5, libactive, libbtn, libbtn1, libpath, libview, libactivity});
// 
//         jPanel4.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "TestCase Source Path"));
// 
//         jLabel8.setText("Path:");
//         jLabel16.setText("Activity:");
//         jLabel17.setText("Activity:");
//         jLabel18.setText("Activity:");
//         jLabel19.setText("Activity:");
//         jLabel20.setText("Activity:");
//         jLabel21.setText("Activity:");
//         jLabel9.setText("View:");
//         tcactive.setText("Active:         ");
//         tcactive.setAlignmentY(0.0F);
//         tcactive.setBorder(null);
//         tcactive.setHorizontalTextPosition(SwingConstants.LEFT);
//         tcbtn1.setText("List Activities");
//         tcbtn.setText("List Views");
//         tcbtn.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listViews(tcview);
//             }
//         });
//         tcbtn1.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listActivities(tcview.getText(),tcactivity);
//             }
//         });
//         GroupLayout jPanel4Layout = new GroupLayout(jPanel4);
//         jPanel4.setLayout(jPanel4Layout);
//         jPanel4Layout.setHorizontalGroup(
//            jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel4Layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                     .addGroup(jPanel4Layout.createSequentialGroup()
//                         .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addComponent(jLabel8)
//                             .addComponent(jLabel9)
//                             .addComponent(jLabel16))
//                         .addGap(18, 18, 18)
//                         .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addGroup(jPanel4Layout.createSequentialGroup()
//                                 .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                                     .addComponent(tcview, javax.swing.GroupLayout.DEFAULT_SIZE, 484, Short.MAX_VALUE)
//                                     .addComponent(tcactivity))
//                                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                                 .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
//                                     .addComponent(tcbtn1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
//                                     .addComponent(tcbtn, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
//                             .addComponent(tcpath)))
//                     .addGroup(jPanel4Layout.createSequentialGroup()
//                         .addComponent(tcactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
//                         .addGap(0, 0, Short.MAX_VALUE)))
//                 .addContainerGap())
//         );
//         jPanel4Layout.setVerticalGroup(
//             jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel4Layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addComponent(tcactive)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel8)
//                     .addComponent(tcpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel9)
//                     .addComponent(tcview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(tcbtn))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(tcbtn1)
//                     .addComponent(tcactivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(jLabel16))
//                 .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
//         );
// 
//         jPanel4Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {jLabel8, jLabel9, tcactive, tcactivity, tcbtn, tcbtn1, tcpath, tcview});
// 
//         jLabel10.setText("Path:");
// 
//         jLabel11.setText("View:");
// 
//         jPanel6.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Test Configuration Path"));
// 
//         jLabel12.setText("Path:");
// 
//         jLabel13.setText("View:");
//         cfgactive.setText("Active:         ");
//         cfgactive.setAlignmentY(0.0F);
//         cfgactive.setBorder(null);
//         cfgactive.setHorizontalTextPosition(SwingConstants.LEFT);
// 
//         cfgbtn.setText("List Views");
//         cfgbtn1.setText("List Activities");
//         cfgbtn.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listViews(cfgview);
//             }
//         });
//         cfgbtn1.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listActivities(cfgview.getText(),cfgactivity);
//             }
//         });
//         GroupLayout jPanel6Layout = new GroupLayout(jPanel6);
//         jPanel6.setLayout(jPanel6Layout);
//         jPanel6Layout.setHorizontalGroup(
//             jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel6Layout.createSequentialGroup()
//                 .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                     .addGroup(jPanel6Layout.createSequentialGroup()
//                         .addGap(10, 10, 10)
//                         .addComponent(cfgactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
//                         .addGap(0, 0, Short.MAX_VALUE))
//                     .addGroup(jPanel6Layout.createSequentialGroup()
//                         .addContainerGap()
//                         .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addComponent(jLabel20)
//                             .addComponent(jLabel13)
//                             .addComponent(jLabel12))
//                         .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
//                         .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addComponent(cfgpath)
//                             .addGroup(jPanel6Layout.createSequentialGroup()
//                                 .addComponent(cfgview)
//                                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                                 .addComponent(cfgbtn))
//                             .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel6Layout.createSequentialGroup()
//                                 .addComponent(cfgactivity)
//                                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                                 .addComponent(cfgbtn1)))))
//                 .addContainerGap())
//         );
//         
//         jPanel6Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {cfgbtn, cfgbtn1});
//         
//         jPanel6Layout.setVerticalGroup(
//             jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel6Layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addComponent(cfgactive)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel12)
//                     .addComponent(cfgpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel13)
//                     .addComponent(cfgview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(cfgbtn))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel20)
//                     .addComponent(cfgactivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(cfgbtn1))
//                 .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
//         );
// 
//         jPanel6Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {cfgactive, cfgactivity, cfgbtn, cfgbtn1, cfgpath, cfgview, jLabel12, jLabel13});
//         
//         jPanel7.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "User SUT Files Path"));
// 
//         jLabel14.setText("Path:");
// 
//         jLabel15.setText("View:");
//         usrsutactive.setText("Active:         ");
//         usrsutactive.setAlignmentY(0.0F);
//         usrsutactive.setBorder(null);
//         usrsutactive.setHorizontalTextPosition(SwingConstants.LEFT);
// 
//         usrsutbtn.setText("List Views");
//         usrsutbtn1.setText("List Activities");
//         usrsutbtn.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listViews(usrsutview);
//             }
//         });
//         usrsutbtn1.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 listActivities(usrsutview.getText(),usractivity);
//             }
//         });
//         GroupLayout jPanel7Layout = new GroupLayout(jPanel7);
//         jPanel7.setLayout(jPanel7Layout);
//         jPanel7Layout.setHorizontalGroup(
//             jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel7Layout.createSequentialGroup()
//                 .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                     .addGroup(jPanel7Layout.createSequentialGroup()
//                         .addGap(10, 10, 10)
//                         .addComponent(usrsutactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
//                         .addGap(0, 0, Short.MAX_VALUE))
//                     .addGroup(jPanel7Layout.createSequentialGroup()
//                         .addContainerGap()
//                         .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addComponent(jLabel21)
//                             .addComponent(jLabel15)
//                             .addComponent(jLabel14))
//                         .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
//                         .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                             .addComponent(usrsutpath)
//                             .addGroup(jPanel7Layout.createSequentialGroup()
//                                 .addComponent(usrsutview)
//                                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                                 .addComponent(usrsutbtn))
//                             .addGroup(jPanel7Layout.createSequentialGroup()
//                                 .addComponent(usractivity)
//                                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                                 .addComponent(usrsutbtn1)))))
//                 .addContainerGap())
//         );
//         
//         jPanel7Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {usrsutbtn, usrsutbtn1});
// 
//         jPanel7Layout.setVerticalGroup(
//             jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(jPanel7Layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addComponent(usrsutactive)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel14)
//                     .addComponent(usrsutpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel15)
//                     .addComponent(usrsutview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(usrsutbtn))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel21)
//                     .addComponent(usractivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                     .addComponent(usrsutbtn1))
//                 .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
//         );
// 
//         jPanel7Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {jLabel14, jLabel15, usrsutactive, usrsutbtn, usrsutbtn1, usrsutpath, usrsutview, usractivity});
// 
//         save.setText("Save");
// 
//         GroupLayout layout = new GroupLayout(main);
//         main.setLayout(layout);
//         layout.setHorizontalGroup(
//             layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                     .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, 669, Short.MAX_VALUE)
//                     .addComponent(jPanel2, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
//                     .addComponent(jPanel5, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
//                     .addComponent(jPanel6, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
//                     .addComponent(jPanel7, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
//                     .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
//                         .addGap(0, 0, Short.MAX_VALUE)
//                         .addComponent(save))
//                     .addGroup(layout.createSequentialGroup()
//                         .addComponent(jLabel3)
//                         .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
//                         .addComponent(type, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
//                     .addComponent(jPanel4, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
//                     .addComponent(jPanel3, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
//                 .addContainerGap())
//         );
//         layout.setVerticalGroup(
//             layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel3)
//                     .addComponent(type, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addComponent(jPanel4, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addComponent(jPanel3, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addComponent(jPanel2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addComponent(jPanel6, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addComponent(jPanel7, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addComponent(jPanel5, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addComponent(save)
//                 .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
//         );
//         
//         save.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 saveConfig();
//             }
//         });
//         
//         type.addItemListener(new ItemListener(){
//             public void itemStateChanged(ItemEvent event) {
//                if (event.getStateChange() == ItemEvent.SELECTED) {
//                   Object item = event.getItem();
//                   if(item.toString().equals("Base")){
//                       jLabel16.setEnabled(false);
//                       jLabel18.setEnabled(false);
//                       jLabel19.setEnabled(false);
//                       jLabel17.setEnabled(false);
//                       jLabel20.setEnabled(false);
//                       jLabel21.setEnabled(false);
//                       tcactivity.setEnabled(false);
//                       projactivity.setEnabled(false);
//                       predefactivity.setEnabled(false);
//                       libactivity.setEnabled(false);
//                       cfgactivity.setEnabled(false);
//                       usractivity.setEnabled(false);
//                       tcbtn1.setEnabled(false);
//                       projbtn1.setEnabled(false);
//                       predefbtn1.setEnabled(false);
//                       libbtn1.setEnabled(false);
//                       cfgbtn1.setEnabled(false);
//                       usrsutbtn1.setEnabled(false);
//                       for(Object ob:change){
//                           if(ob instanceof JButton){
//                               JButton but = (JButton)ob;
//                               but.setText(but.getText().replace("Activities","Views"));
//                               but.setText(but.getText().replace("Activity","View"));
//                           }else{
//                               JLabel lab = (JLabel)ob;
//                               lab.setText(lab.getText().replace("Activities","Views"));
//                               lab.setText(lab.getText().replace("Activity","View"));
//                           }
//                       }
//                   } else {
//                       jLabel16.setEnabled(true);
//                       tcactivity.setEnabled(true);
//                       projactivity.setEnabled(true);
//                       predefactivity.setEnabled(true);
//                       libactivity.setEnabled(true);
//                       cfgactivity.setEnabled(true);
//                       usractivity.setEnabled(true);
//                       tcbtn1.setEnabled(true);
//                       projbtn1.setEnabled(true);
//                       predefbtn1.setEnabled(true);
//                       libbtn1.setEnabled(true);
//                       cfgbtn1.setEnabled(true);
//                       usrsutbtn1.setEnabled(true);
//                       jLabel18.setEnabled(true);
//                       jLabel19.setEnabled(true);
//                       jLabel17.setEnabled(true);
//                       jLabel20.setEnabled(true);
//                       jLabel21.setEnabled(true);
//                       for(Object ob:change){
//                           if(ob instanceof JButton){
//                               JButton but = (JButton)ob;
//                               but.setText(but.getText().replace("Views","Activities"));
//                               but.setText(but.getText().replace("View","Activity"));
//                           }else{
//                               JLabel lab = (JLabel)ob;
//                               lab.setText(lab.getText().replace("Views","Activities"));
//                               lab.setText(lab.getText().replace("View","Activity"));
//                           }
//                       }
//                   }
//                }
//             }       
//         });
//     }
//     
//     /*
//      * get default config xml from server
//      */
//     private Document getRemoteConfigContent(){
//         try{
//             String content = new String(RunnerRepository.getRemoteFileContent(RunnerRepository.USERHOME+"/twister/config/clearcaseconfig.xml",false,null));
//             File file = new File(RunnerRepository.temp+RunnerRepository.getBar()+"Twister"+RunnerRepository.getBar()+"config"+RunnerRepository.getBar()+"clearcaseconfig.xml");
//             if(content==null){
//                 CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
//                     "Warning","Could not get clearcaseconfig.xml from "
//                     +RunnerRepository.USERHOME+"+/twister/config/ creating a blank one.");
//                     saveConfig();
//             } else if(content.indexOf("*ERROR*")!=-1){
//                 CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,main,"ERROR", content);
//                 saveConfig();
//             } else {
//                  BufferedWriter writer = new BufferedWriter(new FileWriter(file));
//                 writer.write(content);
//                 writer.flush();
//                 writer.close();
//             }
//             DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
//             DocumentBuilder db = dbf.newDocumentBuilder();
//             Document doc = db.parse(file);
//             doc.getDocumentElement().normalize();
//             return doc;
//         }catch(Exception e){
//             e.printStackTrace();
//             return null;
//         } 
//     }
//     
//     /*
//      * interpret config xml amd assign saved values
//      */
//     private void interpretConfig(Element root){
//         interpretTag(root.getElementsByTagName("TestCaseSourcePath").item(0),tcactive,tcview,tcpath,tcactivity);
//         interpretTag(root.getElementsByTagName("UsersPath").item(0),projactive,projview,projpath,projactivity);
//         interpretTag(root.getElementsByTagName("PredefinedSuitesPath").item(0),predefactive,predefview,predefpath,predefactivity);
//         interpretTag(root.getElementsByTagName("LibsPath").item(0),libactive,libview,libpath,libactivity);
//         interpretTag(root.getElementsByTagName("TestConfigPath").item(0),cfgactive,cfgview,cfgpath,cfgactivity);
//         interpretTag(root.getElementsByTagName("SutPath").item(0),usrsutactive,usrsutview,usrsutpath,usractivity);
//         try{String ttype = root.getElementsByTagName("Type").item(0).getAttributes().getNamedItem("type").getNodeValue();
//             int size = type.getItemCount();
//             for(int i = 0;i<size;i++){
//                 if(type.getItemAt(i).toString().equals(ttype)){
//                     type.setSelectedIndex(i);
//                     break;
//                 }
//             }
//             if(ttype.equals("Base")){
//                 jLabel16.setEnabled(false);
//                 jLabel18.setEnabled(false);
//                 jLabel19.setEnabled(false);
//                 jLabel17.setEnabled(false);
//                 jLabel20.setEnabled(false);
//                 jLabel21.setEnabled(false);
//                 tcactivity.setEnabled(false);
//                 projactivity.setEnabled(false);
//                 predefactivity.setEnabled(false);
//                 libactivity.setEnabled(false);
//                 cfgactivity.setEnabled(false);
//                 usractivity.setEnabled(false);
//                 tcbtn1.setEnabled(false);
//                 projbtn1.setEnabled(false);
//                 predefbtn1.setEnabled(false);
//                 libbtn1.setEnabled(false);
//                 cfgbtn1.setEnabled(false);
//                 usrsutbtn1.setEnabled(false);
//             }
//         }catch(Exception e){
//             System.out.println("Could not interpret Type tag from clearcaseconfig.xml");
//             e.printStackTrace();
//         }
//     }
//     
//     /*
//      * create and upload config to server
//      */
//     private void saveConfig(){
//         boolean saved = true;
//         try{DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
//             DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
//             Document document = documentBuilder.newDocument();
//             TransformerFactory transformerFactory = TransformerFactory.newInstance();
//             Transformer transformer = transformerFactory.newTransformer();
//             transformer.setOutputProperty(OutputKeys.INDENT, "yes");
//             transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
//             DOMSource source = new DOMSource(document);                    
//             Element root = document.createElement("Root");
//             document.appendChild(root);
//             try{addTag("TestCaseSourcePath",tcactive.isSelected(), tcview.getText(),tcpath.getText(),tcactivity.getText(),root,document);}
//             catch(Exception e){addTag("TestCaseSourcePath",false,"","","",root,document);}
//             try{addTag("UsersPath",projactive.isSelected(), projview.getText(),projpath.getText(),projactivity.getText(),root,document);}
//             catch(Exception e){addTag("UsersPath",false,"","",null,root,document);}
//             try{addTag("PredefinedSuitesPath",predefactive.isSelected(), predefview.getText(),predefpath.getText(),predefactivity.getText(),root,document);}
//             catch(Exception e){addTag("PredefinedSuitesPath",false,"","","",root,document);} 
//             try{addTag("LibsPath",libactive.isSelected(), libview.getText(),libpath.getText(),libactivity.getText(),root,document);}
//             catch(Exception e){addTag("LibsPath",false,"","","",root,document);}
//             try{addTag("TestConfigPath",cfgactive.isSelected(), cfgview.getText(),cfgpath.getText(),cfgactivity.getText(),root,document);}
//             catch(Exception e){addTag("TestConfigPath",false,"","","",root,document);}
//             try{addTag("SutPath",usrsutactive.isSelected(), usrsutview.getText(),usrsutpath.getText(),usractivity.getText(),root,document);}
//             catch(Exception e){addTag("SutPath",false,"","","",root,document);}
//             Element rootElement = document.createElement("Type");
//             rootElement.setAttribute("type",type.getSelectedItem().toString());
//             root.appendChild(rootElement);
//             File file = new File(RunnerRepository.temp+RunnerRepository.getBar()+
//                                 "Twister"+RunnerRepository.getBar()+"config"+RunnerRepository.getBar()+"clearcaseconfig.xml");
//             Result result = new StreamResult(file);
//             transformer.transform(source, result);
//             FileInputStream in = new FileInputStream(file);
//             RunnerRepository.uploadRemoteFile(RunnerRepository.USERHOME+"/twister/config/", in,null, "clearcaseconfig.xml",false,null);
//             System.out.println("saveconf:"+file.getAbsolutePath());
//         }
//         catch(ParserConfigurationException e){
//             System.out.println("DocumentBuilder cannot be created which"+
//                                 " satisfies the configuration requested");
//             saved = false;}
//         catch(TransformerConfigurationException e){
//             System.out.println("Could not create transformer");
//             saved = false;}
//         catch(Exception e){
//             e.printStackTrace();
//             saved = false;}
//         if(saved){
//             CustomDialog.showInfo(JOptionPane.INFORMATION_MESSAGE,
//                                   RunnerRepository.window,
//                                   "Successful", "File successfully saved");}
//         else{
//             CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,
//                                   RunnerRepository.window.mainpanel.p4.getConfig(),
//                                   "Warning", "File could not be saved ");
//         }
//     }
//     
//     /*
//      * convenient method to interpret tag and assign value to coresponding field
//      */
//     private void interpretTag(Node tag, JCheckBox check, JTextField view,JTextField path,JTextField activity){
//             try{String active = tag.getAttributes().getNamedItem("active").getNodeValue();
//                 check.setSelected(Boolean.parseBoolean(active));
//             } catch(Exception e){
//                 System.out.println("ClearCase config active not found");
//             }
//             try{String tview = tag.getAttributes().getNamedItem("view").getNodeValue();
//                 view.setText(tview);
//             } catch(Exception e){
//                 System.out.println("ClearCase config view not found");
//                 view.setText("");
//             }
//             try{String tpath = tag.getAttributes().getNamedItem("path").getNodeValue();
//                 path.setText(tpath);
//             } catch(Exception e){
//                 System.out.println("ClearCase config path not found");
//                 path.setText("");
//             }
//             try{
//                 if(activity!=null)activity.setText(tag.getAttributes().getNamedItem("activity").getNodeValue());
//             } catch(Exception e){
//                 System.out.println("ClearCase config activity not found");
//                 activity.setText("");
//             }
//     }
//     
//     /*
//      * create specifig tag used in config xml
//      */
//     private void addTag(String tagname, boolean active, String view, String path,String activity,
//                               Element root,Document document){
//         Element rootElement = document.createElement(tagname);
//         rootElement.setAttribute("active",active+"");
//         rootElement.setAttribute("view",view);
//         if(activity!=null)rootElement.setAttribute("activity",activity);
//         rootElement.setAttribute("path",path);
//         root.appendChild(rootElement);
//     }
//     
//     /*
//      * interpret type based on selected value
//      * Base = 0; UCM = 1
//      */
//     public int getType(){
//         if(type.getSelectedItem().toString().equals("Base")){
//             return 0;
//         }
//         return 1;
//     }
//     
//     /*
//      * list activities based on clearcase command
//      * and assign selection to field
//      */
//     public String listActivities(String view,JTextField tf){
//         if(view.equals("")){
//             CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCaseConfig.this,
//                                         "Error", "Please set view before listing activities!");
//             return "";
//         }
//         HashMap<String, String> hash = new HashMap<String, String>();
//         hash.put("view", view);
//         hash.put("command", "lsactivity");
//         String resp = cc.sendCommand(hash,false).toString();
//         if(resp.indexOf("*ERROR*")!=-1){
//             CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCaseConfig.this,"Error", resp);
//             return "";
//         }
//         String [] activities = resp.split("\n");
//         JPanel libraries = new JPanel();
//         JScrollPane jScrollPane1 = new JScrollPane();
//         final JList jList1 = new JList();
//         jScrollPane1.setViewportView(jList1);
//         GroupLayout layout = new GroupLayout(libraries);
//         libraries.setLayout(layout);
//         layout.setHorizontalGroup(
//             layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGroup(layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                     .addComponent(jScrollPane1))
//                 .addContainerGap())
//         );
//         layout.setVerticalGroup(
//             layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
//                 .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 247, Short.MAX_VALUE)
//                 .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
//                 .addContainerGap())
//         );
//         jList1.setModel(new DefaultComboBoxModel(activities));
//         
//         int respons = (Integer)CustomDialog.showDialog(libraries,JOptionPane.PLAIN_MESSAGE,
//                                                         JOptionPane.OK_CANCEL_OPTION, 
//                                                         RunnerRepository.window, "Activities",
//                                                         null);
//         if(respons == JOptionPane.OK_OPTION){
//             if(jList1.getSelectedIndex()==-1){
//                 CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCaseConfig.this,
//                                         "Error", "Please select one activity");
//                 return "";
//             }
//             String selectedactivity = jList1.getSelectedValue().toString();
//             if(tf!=null)tf.setText(selectedactivity);
//             return selectedactivity;
//         }
//         return "";
//     }
//     
//     /*
//      * list views based on clearcase command
//      * and assign selection to field
//      */
//     public String listViews(JTextField tf){
//         HashMap<String, String> hash = new HashMap<String, String>();
//         hash.put("command", " cleartool lsview -short | grep "+RunnerRepository.user);
//         String [] resp = cc.sendCommand(hash,false).split("\n");
//         JPanel libraries = new JPanel();
//         JScrollPane jScrollPane1 = new JScrollPane();
//         final JList jList1 = new JList();
//         JLabel filter = new JLabel("List View Filter:");
//         final JTextField tfilter = new JTextField();
//         tfilter.setText(RunnerRepository.user);
//         JButton refresh = new JButton("Refresh");
//         jScrollPane1.setViewportView(jList1);
//         GroupLayout layout = new GroupLayout(libraries);
//         libraries.setLayout(layout);
//         layout.setHorizontalGroup(
//             layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGroup(layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                     .addGroup(layout.createSequentialGroup()
//                         .addComponent(filter)
//                         .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
//                         .addComponent(tfilter, GroupLayout.PREFERRED_SIZE, 149, GroupLayout.PREFERRED_SIZE)
//                         .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
//                         .addComponent(refresh)
//                         .addGap(0, 0, Short.MAX_VALUE))
//                     .addComponent(jScrollPane1))
//                 .addContainerGap())
//         );
//         layout.setVerticalGroup(
//             layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
//                     .addComponent(filter)
//                     .addComponent(tfilter, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
//                     .addComponent(refresh))
//                 .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
//                 .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 247, Short.MAX_VALUE)
//                 .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
//                 .addContainerGap())
//         );
//         
//         layout.linkSize(SwingConstants.VERTICAL, new Component[] {refresh, tfilter});
//         jList1.setModel(new DefaultComboBoxModel(resp));
//         
//         refresh.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 new Thread(){
//                     public void run(){
//                        String filter = tfilter.getText();
//                         String [] resp = null;
//                         String command = "";
//                         if(filter.equals("")){
//                             command = " cleartool lsview -short ";
//                         } else {
//                             command = " cleartool lsview -short | grep "+filter;
//                         }
//                         HashMap<String, String> hash = new HashMap<String, String>();
//                         hash.put("command", command);
//                         resp = cc.sendCommand(hash,false).split("\n");
//                         jList1.setModel(new DefaultComboBoxModel(resp)); 
//                     }
//                 }.start();
//         }});
//         
//         int respons = (Integer)CustomDialog.showDialog(libraries,JOptionPane.PLAIN_MESSAGE,
//                                                         JOptionPane.OK_CANCEL_OPTION, 
//                                                         RunnerRepository.window, "Views",
//                                                         null);
//         if(respons == JOptionPane.OK_OPTION){
//             if(jList1.getSelectedIndex()==-1){
//                 CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCaseConfig.this,
//                                         "Error", "Please select one view!");
//                 return "";
//             }
//             String view = jList1.getSelectedValue().toString();
//             if(tf!=null)tf.setText(view);
//             return view;
//         }
//         return "";
//     }
// }



















import javax.swing.JPanel;
import java.awt.Color;
import javax.swing.GroupLayout;
import javax.swing.BorderFactory;
import javax.swing.SwingConstants;
import javax.swing.JLabel;
import javax.swing.LayoutStyle;
import org.w3c.dom.Element;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import javax.swing.JOptionPane;
import com.twister.CustomDialog;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.dom.DOMSource;
import java.io.File;
import java.io.FileInputStream;
import javax.xml.transform.Result;
import javax.xml.transform.stream.StreamResult;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerConfigurationException;
import javax.swing.JCheckBox;
import javax.swing.JTextField;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JScrollPane;
import java.util.ArrayList;
import javax.swing.JButton;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import java.util.HashMap;
import javax.swing.JList;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JComboBox;
import java.awt.Component;


public class ClearCaseConfig extends JPanel{
    private JPanel main;
    private JLabel jLabel,jLabel1,jLabel10,jLabel11,jLabel12,
                   jLabel13,jLabel14,jLabel15,jLabel2,
                   jLabel3,jLabel4,jLabel5,jLabel6,jLabel7,
                   jLabel8,jLabel9,jLabel16,jPanel5,jLabel17,
                   jLabel18,jLabel19,jLabel20,jLabel21;
    private JPanel jPanel1,jPanel2,jPanel3,
                   jPanel4,jPanel6,jPanel7;
    private JButton libbtn,predefbtn,usrsutbtn,cfgbtn,
                    tcbtn,save,projbtn,tcbtn1,projbtn1,predefbtn1,
                    libbtn1,cfgbtn1,usrsutbtn1;
    private JTextField libpath,predefpath,predefview,
                       tcpath,tcview,cfgview,cfgpath,projpath,
                       usrsutpath,usrsutview,libview,projview,tcactivity,projactivity,
                       libactivity,predefactivity,cfgactivity,usractivity;
    private JCheckBox tcactive,predefactive,projactive,libactive,usrsutactive,cfgactive;
    private JComboBox type;
    public ArrayList change;//array to hold items that change based on type
    private ClearCase cc;
    
    public ClearCaseConfig(ClearCase cc){
        this.cc = cc;
        initComponents();
        interpretConfig((Element)getRemoteConfigContent().getFirstChild());
    }
    
    
    private void initComponents() { 
        tcbtn1 = new JButton();
        projbtn1 = new JButton();
        predefbtn1 = new JButton();
        libbtn1 = new JButton();
        cfgbtn1 = new JButton();
        usrsutbtn1 = new JButton();
        main = new JPanel();
        add(main);
        jPanel1 = new JPanel();
        jLabel1 = new JLabel();
        jLabel21 = new JLabel();
        jLabel2 = new JLabel();
        jPanel5 = new JLabel();
        jLabel18 = new JLabel();
        jLabel19 = new JLabel();
        jLabel20 = new JLabel();
        projpath = new JTextField();
        tcactivity = new JTextField();
        predefactivity = new JTextField();
        projactivity = new JTextField();
        cfgactivity = new JTextField();
        libactivity = new JTextField();
        projview = new JTextField();
        usractivity = new JTextField();
        projactive = new JCheckBox();
        projbtn = new JButton();
        jLabel3 = new JLabel();
        type = new JComboBox();
        jPanel3 = new JPanel();
        jLabel6 = new JLabel();
        jLabel7 = new JLabel();
        jLabel17 = new JLabel();
        predefpath = new JTextField();
        predefview = new JTextField();
        predefactive = new JCheckBox();
        predefbtn = new JButton();
        jPanel2 = new JPanel();
        jLabel4 = new JLabel();
        jLabel5 = new JLabel();
        libpath = new JTextField();
        libview = new JTextField();
        libactive = new JCheckBox();
        libbtn = new JButton();
        jPanel4 = new JPanel();
        jLabel8 = new JLabel();
        jLabel9 = new JLabel();
        tcpath = new JTextField();
        tcview = new JTextField();
        tcactive = new JCheckBox();
        tcbtn = new JButton();
        jLabel10 = new JLabel();
        jLabel11 = new JLabel();
        jPanel6 = new JPanel();
        jLabel12 = new JLabel();
        jLabel13 = new JLabel();
        cfgpath = new JTextField();
        cfgview = new JTextField();
        cfgactive = new JCheckBox();
        cfgbtn = new JButton();
        jPanel7 = new JPanel();
        jLabel14 = new JLabel();
        jLabel15 = new JLabel();
        jLabel16 = new JLabel();
        usrsutpath = new JTextField();
        usrsutview = new JTextField();
        usrsutactive = new JCheckBox();
        usrsutbtn = new JButton();
        save = new JButton();
        change = new ArrayList();
        jPanel1.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Projects Path"));

        jLabel1.setText("Path:");

        jLabel2.setText("View:");
        projactive.setText("Active:         ");
        projactive.setAlignmentY(0.0F);
        projactive.setBorder(null);
        projactive.setHorizontalTextPosition(SwingConstants.LEFT);

        projbtn1.setText("List Activities");
        projbtn.setText("List Views");
        projbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(projview);
            }
        });
        projbtn1.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listActivities(projview.getText(),projactivity);
            }
        });
        GroupLayout jPanel1Layout = new GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(projactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel1)
                            .addComponent(jLabel2)
                            .addComponent(jLabel17))
                        .addGap(18, 18, 18)
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                                .addComponent(projview)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(projbtn, javax.swing.GroupLayout.PREFERRED_SIZE, 90, javax.swing.GroupLayout.PREFERRED_SIZE))
                            .addGroup(jPanel1Layout.createSequentialGroup()
                                .addComponent(projactivity)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(projbtn1))
                            .addComponent(projpath))))
                .addContainerGap())
        );
        jPanel1Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {projbtn, projbtn1});
        
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addGap(10, 10, 10)
                .addComponent(projactive)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel1)
                    .addComponent(projpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel2)
                    .addComponent(projview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(projbtn))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel17)
                    .addComponent(projactivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(projbtn1))
                .addContainerGap(12, Short.MAX_VALUE))
        );

        jPanel1Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {jLabel1, jLabel2, projactive, projactivity, projbtn, projbtn1, projpath, projview});

        jLabel3.setText("Type:");

        type.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Base", "UCM" }));

        jPanel3.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Predefined Suites Path"));

        jLabel6.setText("Path:");

        jLabel7.setText("View:");
        predefactive.setText("Active:         ");
        predefactive.setAlignmentY(0.0F);
        predefactive.setBorder(null);
        predefactive.setHorizontalTextPosition(SwingConstants.LEFT);

        predefbtn.setText("List Views");
        predefbtn1.setText("List Activities");
        predefbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(predefview);
            }
        });
        predefbtn1.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listActivities(predefview.getText(),predefactivity);
            }
        });
        GroupLayout jPanel3Layout = new GroupLayout(jPanel3);
        jPanel3.setLayout(jPanel3Layout);
        jPanel3Layout.setHorizontalGroup(
            jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel3Layout.createSequentialGroup()
                .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel3Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(predefactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addGroup(jPanel3Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel18)
                            .addComponent(jLabel7)
                            .addComponent(jLabel6))
                        .addGap(18, 18, 18)
                        .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(predefpath)
                            .addGroup(jPanel3Layout.createSequentialGroup()
                                .addComponent(predefview)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(predefbtn))
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel3Layout.createSequentialGroup()
                                .addComponent(predefactivity)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(predefbtn1)))))
                .addContainerGap())
        );
        
        jPanel3Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {predefbtn, predefbtn1});
        
        jPanel3Layout.setVerticalGroup(
            jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel3Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(predefactive)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel6)
                    .addComponent(predefpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel7)
                    .addComponent(predefview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(predefbtn))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel18)
                    .addComponent(predefactivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(predefbtn1))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        
        jPanel3Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {jLabel6, jLabel7, predefactive, predefactivity, predefbtn, predefbtn1, predefpath, predefview});
        
        jPanel2.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Library Path"));
        
        jLabel4.setText("Path:");

        jLabel5.setText("View:");
        libactive.setText("Active:         ");
        libactive.setAlignmentY(0.0F);
        libactive.setBorder(null);
        libactive.setHorizontalTextPosition(SwingConstants.LEFT);

        libbtn.setText("List Views");
        libbtn1.setText("List Activities");
        libbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(libview);
            }
        });
        libbtn1.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listActivities(libview.getText(),libactivity);
            }
        });
        GroupLayout jPanel2Layout = new GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(libactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel5)
                            .addComponent(jLabel19)
                            .addComponent(jLabel4))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel2Layout.createSequentialGroup()
                                .addComponent(libview)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(libbtn))
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel2Layout.createSequentialGroup()
                                .addComponent(libactivity)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(libbtn1))
                            .addComponent(libpath))))
                .addContainerGap())
        );
        
        jPanel2Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {libbtn, libbtn1});

        
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(libactive)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel4)
                    .addComponent(libpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel5)
                    .addComponent(libview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(libbtn))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel19)
                    .addComponent(libactivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(libbtn1))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        jPanel2Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {jLabel4, jLabel5, libactive, libbtn, libbtn1, libpath, libview, libactivity});

        jPanel4.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "TestCase Source Path"));

        jLabel8.setText("Path:");
        jLabel16.setText("Activity:");
        jLabel17.setText("Activity:");
        jLabel18.setText("Activity:");
        jLabel19.setText("Activity:");
        jLabel20.setText("Activity:");
        jLabel21.setText("Activity:");
        jLabel9.setText("View:");
        tcactive.setText("Active:         ");
        tcactive.setAlignmentY(0.0F);
        tcactive.setBorder(null);
        tcactive.setHorizontalTextPosition(SwingConstants.LEFT);
        tcbtn1.setText("List Activities");
        tcbtn.setText("List Views");
        tcbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(tcview);
            }
        });
        tcbtn1.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listActivities(tcview.getText(),tcactivity);
            }
        });
        GroupLayout jPanel4Layout = new GroupLayout(jPanel4);
        jPanel4.setLayout(jPanel4Layout);
        jPanel4Layout.setHorizontalGroup(
           jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel4Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel4Layout.createSequentialGroup()
                        .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel8)
                            .addComponent(jLabel9)
                            .addComponent(jLabel16))
                        .addGap(18, 18, 18)
                        .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(jPanel4Layout.createSequentialGroup()
                                .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(tcview, javax.swing.GroupLayout.DEFAULT_SIZE, 484, Short.MAX_VALUE)
                                    .addComponent(tcactivity))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                                    .addComponent(tcbtn1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                    .addComponent(tcbtn, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))
                            .addComponent(tcpath)))
                    .addGroup(jPanel4Layout.createSequentialGroup()
                        .addComponent(tcactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 0, Short.MAX_VALUE)))
                .addContainerGap())
        );
        jPanel4Layout.setVerticalGroup(
            jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel4Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(tcactive)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel8)
                    .addComponent(tcpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel9)
                    .addComponent(tcview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(tcbtn))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(tcbtn1)
                    .addComponent(tcactivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel16))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        jPanel4Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {jLabel8, jLabel9, tcactive, tcactivity, tcbtn, tcbtn1, tcpath, tcview});

        jLabel10.setText("Path:");

        jLabel11.setText("View:");

        jPanel6.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Test Configuration Path"));

        jLabel12.setText("Path:");

        jLabel13.setText("View:");
        cfgactive.setText("Active:         ");
        cfgactive.setAlignmentY(0.0F);
        cfgactive.setBorder(null);
        cfgactive.setHorizontalTextPosition(SwingConstants.LEFT);

        cfgbtn.setText("List Views");
        cfgbtn1.setText("List Activities");
        cfgbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(cfgview);
            }
        });
        cfgbtn1.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listActivities(cfgview.getText(),cfgactivity);
            }
        });
        GroupLayout jPanel6Layout = new GroupLayout(jPanel6);
        jPanel6.setLayout(jPanel6Layout);
        jPanel6Layout.setHorizontalGroup(
            jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel6Layout.createSequentialGroup()
                .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel6Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(cfgactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addGroup(jPanel6Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel20)
                            .addComponent(jLabel13)
                            .addComponent(jLabel12))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(cfgpath)
                            .addGroup(jPanel6Layout.createSequentialGroup()
                                .addComponent(cfgview)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(cfgbtn))
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel6Layout.createSequentialGroup()
                                .addComponent(cfgactivity)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(cfgbtn1)))))
                .addContainerGap())
        );
        
        jPanel6Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {cfgbtn, cfgbtn1});
        
        jPanel6Layout.setVerticalGroup(
            jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel6Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(cfgactive)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel12)
                    .addComponent(cfgpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel13)
                    .addComponent(cfgview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(cfgbtn))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel6Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel20)
                    .addComponent(cfgactivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(cfgbtn1))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        jPanel6Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {cfgactive, cfgactivity, cfgbtn, cfgbtn1, cfgpath, cfgview, jLabel12, jLabel13});
        
        jPanel7.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "User SUT Files Path"));

        jLabel14.setText("Path:");

        jLabel15.setText("View:");
        usrsutactive.setText("Active:         ");
        usrsutactive.setAlignmentY(0.0F);
        usrsutactive.setBorder(null);
        usrsutactive.setHorizontalTextPosition(SwingConstants.LEFT);

        usrsutbtn.setText("List Views");
        usrsutbtn1.setText("List Activities");
        usrsutbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(usrsutview);
            }
        });
        usrsutbtn1.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listActivities(usrsutview.getText(),usractivity);
            }
        });
        GroupLayout jPanel7Layout = new GroupLayout(jPanel7);
        jPanel7.setLayout(jPanel7Layout);
        jPanel7Layout.setHorizontalGroup(
            jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel7Layout.createSequentialGroup()
                .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel7Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(usrsutactive, javax.swing.GroupLayout.PREFERRED_SIZE, 115, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addGroup(jPanel7Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel21)
                            .addComponent(jLabel15)
                            .addComponent(jLabel14))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(usrsutpath)
                            .addGroup(jPanel7Layout.createSequentialGroup()
                                .addComponent(usrsutview)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(usrsutbtn))
                            .addGroup(jPanel7Layout.createSequentialGroup()
                                .addComponent(usractivity)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(usrsutbtn1)))))
                .addContainerGap())
        );
        
        jPanel7Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {usrsutbtn, usrsutbtn1});

        jPanel7Layout.setVerticalGroup(
            jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel7Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(usrsutactive)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel14)
                    .addComponent(usrsutpath, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel15)
                    .addComponent(usrsutview, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(usrsutbtn))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel7Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel21)
                    .addComponent(usractivity, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(usrsutbtn1))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        jPanel7Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {jLabel14, jLabel15, usrsutactive, usrsutbtn, usrsutbtn1, usrsutpath, usrsutview, usractivity});

        save.setText("Save");

        GroupLayout layout = new GroupLayout(main);
        main.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, 669, Short.MAX_VALUE)
                    .addComponent(jPanel2, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jPanel5, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jPanel6, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jPanel7, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addGap(0, 0, Short.MAX_VALUE)
                        .addComponent(save))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jLabel3)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(type, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addComponent(jPanel4, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jPanel3, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel3)
                    .addComponent(type, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel4, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel3, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel6, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel7, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel5, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(save)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        
        save.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                saveConfig();
            }
        });
        
        type.addItemListener(new ItemListener(){
            public void itemStateChanged(ItemEvent event) {
               if (event.getStateChange() == ItemEvent.SELECTED) {
                  Object item = event.getItem();
                  if(item.toString().equals("Base")){
                      jLabel16.setEnabled(false);
                      jLabel18.setEnabled(false);
                      jLabel19.setEnabled(false);
                      jLabel17.setEnabled(false);
                      jLabel20.setEnabled(false);
                      jLabel21.setEnabled(false);
                      tcactivity.setEnabled(false);
                      projactivity.setEnabled(false);
                      predefactivity.setEnabled(false);
                      libactivity.setEnabled(false);
                      cfgactivity.setEnabled(false);
                      usractivity.setEnabled(false);
                      tcbtn1.setEnabled(false);
                      projbtn1.setEnabled(false);
                      predefbtn1.setEnabled(false);
                      libbtn1.setEnabled(false);
                      cfgbtn1.setEnabled(false);
                      usrsutbtn1.setEnabled(false);
                      for(Object ob:change){
                          if(ob instanceof JButton){
                              JButton but = (JButton)ob;
                              but.setText(but.getText().replace("Activities","Views"));
                              but.setText(but.getText().replace("Activity","View"));
                          }else{
                              JLabel lab = (JLabel)ob;
                              lab.setText(lab.getText().replace("Activities","Views"));
                              lab.setText(lab.getText().replace("Activity","View"));
                          }
                      }
                  } else {
                      jLabel16.setEnabled(true);
                      tcactivity.setEnabled(true);
                      projactivity.setEnabled(true);
                      predefactivity.setEnabled(true);
                      libactivity.setEnabled(true);
                      cfgactivity.setEnabled(true);
                      usractivity.setEnabled(true);
                      tcbtn1.setEnabled(true);
                      projbtn1.setEnabled(true);
                      predefbtn1.setEnabled(true);
                      libbtn1.setEnabled(true);
                      cfgbtn1.setEnabled(true);
                      usrsutbtn1.setEnabled(true);
                      jLabel18.setEnabled(true);
                      jLabel19.setEnabled(true);
                      jLabel17.setEnabled(true);
                      jLabel20.setEnabled(true);
                      jLabel21.setEnabled(true);
                      for(Object ob:change){
                          if(ob instanceof JButton){
                              JButton but = (JButton)ob;
                              but.setText(but.getText().replace("Views","Activities"));
                              but.setText(but.getText().replace("View","Activity"));
                          }else{
                              JLabel lab = (JLabel)ob;
                              lab.setText(lab.getText().replace("Views","Activities"));
                              lab.setText(lab.getText().replace("View","Activity"));
                          }
                      }
                  }
               }
            }       
        });
    }
    
    /*
     * get default config xml from server
     */
    private Document getRemoteConfigContent(){
        try{
            String content = new String(RunnerRepository.getRemoteFileContent(RunnerRepository.USERHOME+"/twister/config/clearcaseconfig.xml",false,null));
            File file = new File(RunnerRepository.temp+RunnerRepository.getBar()+"Twister"+RunnerRepository.getBar()+"config"+RunnerRepository.getBar()+"clearcaseconfig.xml");
            if(content==null){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,main,
                    "Warning","Could not get clearcaseconfig.xml from "
                    +RunnerRepository.USERHOME+"+/twister/config/ creating a blank one.");
                    saveConfig();
            } else if(content.indexOf("*ERROR*")!=-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,main,"ERROR", content);
                saveConfig();
            } else {
                 BufferedWriter writer = new BufferedWriter(new FileWriter(file));
                writer.write(content);
                writer.flush();
                writer.close();
            }
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            Document doc = db.parse(file);
            doc.getDocumentElement().normalize();
            return doc;
        }catch(Exception e){
            e.printStackTrace();
            return null;
        } 
    }
    
    /*
     * interpret config xml amd assign saved values
     */
    private void interpretConfig(Element root){
        interpretTag(root.getElementsByTagName("TestCaseSourcePath").item(0),tcactive,tcview,tcpath,tcactivity);
        interpretTag(root.getElementsByTagName("UsersPath").item(0),projactive,projview,projpath,projactivity);
        interpretTag(root.getElementsByTagName("PredefinedSuitesPath").item(0),predefactive,predefview,predefpath,predefactivity);
        interpretTag(root.getElementsByTagName("LibsPath").item(0),libactive,libview,libpath,libactivity);
        interpretTag(root.getElementsByTagName("TestConfigPath").item(0),cfgactive,cfgview,cfgpath,cfgactivity);
        interpretTag(root.getElementsByTagName("SutPath").item(0),usrsutactive,usrsutview,usrsutpath,usractivity);
        try{String ttype = root.getElementsByTagName("Type").item(0).getAttributes().getNamedItem("type").getNodeValue();
            int size = type.getItemCount();
            for(int i = 0;i<size;i++){
                if(type.getItemAt(i).toString().equals(ttype)){
                    type.setSelectedIndex(i);
                    break;
                }
            }
            if(ttype.equals("Base")){
                jLabel16.setEnabled(false);
                jLabel18.setEnabled(false);
                jLabel19.setEnabled(false);
                jLabel17.setEnabled(false);
                jLabel20.setEnabled(false);
                jLabel21.setEnabled(false);
                tcactivity.setEnabled(false);
                projactivity.setEnabled(false);
                predefactivity.setEnabled(false);
                libactivity.setEnabled(false);
                cfgactivity.setEnabled(false);
                usractivity.setEnabled(false);
                tcbtn1.setEnabled(false);
                projbtn1.setEnabled(false);
                predefbtn1.setEnabled(false);
                libbtn1.setEnabled(false);
                cfgbtn1.setEnabled(false);
                usrsutbtn1.setEnabled(false);
            }
        }catch(Exception e){
            System.out.println("Could not interpret Type tag from clearcaseconfig.xml");
            e.printStackTrace();
        }
    }
    
    /*
     * create and upload config to server
     */
    private void saveConfig(){
        boolean saved = true;
        try{DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
            Document document = documentBuilder.newDocument();
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            DOMSource source = new DOMSource(document);                    
            Element root = document.createElement("Root");
            document.appendChild(root);
            try{addTag("TestCaseSourcePath",tcactive.isSelected(), tcview.getText(),tcpath.getText(),tcactivity.getText(),root,document);}
            catch(Exception e){addTag("TestCaseSourcePath",false,"","","",root,document);}
            try{addTag("UsersPath",projactive.isSelected(), projview.getText(),projpath.getText(),projactivity.getText(),root,document);}
            catch(Exception e){addTag("UsersPath",false,"","",null,root,document);}
            try{addTag("PredefinedSuitesPath",predefactive.isSelected(), predefview.getText(),predefpath.getText(),predefactivity.getText(),root,document);}
            catch(Exception e){addTag("PredefinedSuitesPath",false,"","","",root,document);} 
            try{addTag("LibsPath",libactive.isSelected(), libview.getText(),libpath.getText(),libactivity.getText(),root,document);}
            catch(Exception e){addTag("LibsPath",false,"","","",root,document);}
            try{addTag("TestConfigPath",cfgactive.isSelected(), cfgview.getText(),cfgpath.getText(),cfgactivity.getText(),root,document);}
            catch(Exception e){addTag("TestConfigPath",false,"","","",root,document);}
            try{addTag("SutPath",usrsutactive.isSelected(), usrsutview.getText(),usrsutpath.getText(),usractivity.getText(),root,document);}
            catch(Exception e){addTag("SutPath",false,"","","",root,document);}
            Element rootElement = document.createElement("Type");
            rootElement.setAttribute("type",type.getSelectedItem().toString());
            root.appendChild(rootElement);
            File file = new File(RunnerRepository.temp+RunnerRepository.getBar()+
                                "Twister"+RunnerRepository.getBar()+"config"+RunnerRepository.getBar()+"clearcaseconfig.xml");
            Result result = new StreamResult(file);
            transformer.transform(source, result);
            FileInputStream in = new FileInputStream(file);
            RunnerRepository.uploadRemoteFile(RunnerRepository.USERHOME+"/twister/config/", in,null, "clearcaseconfig.xml",false,null);
            System.out.println("saveconf:"+file.getAbsolutePath());
        }
        catch(ParserConfigurationException e){
            System.out.println("DocumentBuilder cannot be created which"+
                                " satisfies the configuration requested");
            saved = false;}
        catch(TransformerConfigurationException e){
            System.out.println("Could not create transformer");
            saved = false;}
        catch(Exception e){
            e.printStackTrace();
            saved = false;}
        if(saved){
            CustomDialog.showInfo(JOptionPane.INFORMATION_MESSAGE,
                                  RunnerRepository.window,
                                  "Successful", "File successfully saved");}
        else{
            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,
                                  RunnerRepository.window.mainpanel.p4.getConfig(),
                                  "Warning", "File could not be saved ");
        }
    }
    
    /*
     * convenient method to interpret tag and assign value to coresponding field
     */
    private void interpretTag(Node tag, JCheckBox check, JTextField view,JTextField path,JTextField activity){
            try{String active = tag.getAttributes().getNamedItem("active").getNodeValue();
                check.setSelected(Boolean.parseBoolean(active));
            } catch(Exception e){
                System.out.println("ClearCase config active not found");
            }
            try{String tview = tag.getAttributes().getNamedItem("view").getNodeValue();
                view.setText(tview);
            } catch(Exception e){
                System.out.println("ClearCase config view not found");
                view.setText("");
            }
            try{String tpath = tag.getAttributes().getNamedItem("path").getNodeValue();
                path.setText(tpath);
            } catch(Exception e){
                System.out.println("ClearCase config path not found");
                path.setText("");
            }
            try{
                if(activity!=null)activity.setText(tag.getAttributes().getNamedItem("activity").getNodeValue());
            } catch(Exception e){
                System.out.println("ClearCase config activity not found");
                activity.setText("");
            }
    }
    
    /*
     * create specifig tag used in config xml
     */
    private void addTag(String tagname, boolean active, String view, String path,String activity,
                              Element root,Document document){
        Element rootElement = document.createElement(tagname);
        rootElement.setAttribute("active",active+"");
        rootElement.setAttribute("view",view);
        if(activity!=null)rootElement.setAttribute("activity",activity);
        rootElement.setAttribute("path",path);
        root.appendChild(rootElement);
    }
    
    /*
     * interpret type based on selected value
     * Base = 0; UCM = 1
     */
    public int getType(){
        if(type.getSelectedItem().toString().equals("Base")){
            return 0;
        }
        return 1;
    }
    
    /*
     * list activities based on clearcase command
     * and assign selection to field
     */
    public String listActivities(String view,JTextField tf){
        if(view.equals("")){
            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCaseConfig.this,
                                        "Error", "Please set view before listing activities!");
            return "";
        }
        HashMap<String, String> hash = new HashMap<String, String>();
        hash.put("view", view);
        hash.put("command", "lsactivity");
        String resp = cc.sendCommand(hash,false).toString();
        if(resp.indexOf("*ERROR*")!=-1){
            CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCaseConfig.this,"Error", resp);
            return "";
        }
        String [] activities = resp.split("\n");
        JPanel libraries = new JPanel();
        JScrollPane jScrollPane1 = new JScrollPane();
        final JList jList1 = new JList();
        jScrollPane1.setViewportView(jList1);
        GroupLayout layout = new GroupLayout(libraries);
        libraries.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(jScrollPane1))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 247, Short.MAX_VALUE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addContainerGap())
        );
        jList1.setModel(new DefaultComboBoxModel(activities));
        
        int respons = (Integer)CustomDialog.showDialog(libraries,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Activities",
                                                        null);
        if(respons == JOptionPane.OK_OPTION){
            if(jList1.getSelectedIndex()==-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCaseConfig.this,
                                        "Error", "Please select one activity");
                return "";
            }
            String selectedactivity = jList1.getSelectedValue().toString();
            if(tf!=null)tf.setText(selectedactivity);
            return selectedactivity;
        }
        return "";
    }
    
    /*
     * list views based on clearcase command
     * and assign selection to field
     */
    public String listViews(JTextField tf){
        HashMap<String, String> hash = new HashMap<String, String>();
        hash.put("command", " cleartool lsview -short | grep "+RunnerRepository.user);
        String [] resp = cc.sendCommand(hash,false).split("\n");
        JPanel libraries = new JPanel();
        JScrollPane jScrollPane1 = new JScrollPane();
        final JList jList1 = new JList();
        JLabel filter = new JLabel("List View Filter:");
        final JTextField tfilter = new JTextField();
        tfilter.setText(RunnerRepository.user);
        JButton refresh = new JButton("Refresh");
        jScrollPane1.setViewportView(jList1);
        GroupLayout layout = new GroupLayout(libraries);
        libraries.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(filter)
                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(tfilter, GroupLayout.PREFERRED_SIZE, 149, GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(refresh)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addComponent(jScrollPane1))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(filter)
                    .addComponent(tfilter, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(refresh))
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jScrollPane1, GroupLayout.DEFAULT_SIZE, 247, Short.MAX_VALUE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addContainerGap())
        );
        
        layout.linkSize(SwingConstants.VERTICAL, new Component[] {refresh, tfilter});
        jList1.setModel(new DefaultComboBoxModel(resp));
        
        refresh.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                new Thread(){
                    public void run(){
                       String filter = tfilter.getText();
                        String [] resp = null;
                        String command = "";
                        if(filter.equals("")){
                            command = " cleartool lsview -short ";
                        } else {
                            command = " cleartool lsview -short | grep "+filter;
                        }
                        HashMap<String, String> hash = new HashMap<String, String>();
                        hash.put("command", command);
                        resp = cc.sendCommand(hash,false).split("\n");
                        jList1.setModel(new DefaultComboBoxModel(resp)); 
                    }
                }.start();
        }});
        
        int respons = (Integer)CustomDialog.showDialog(libraries,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Views",
                                                        null);
        if(respons == JOptionPane.OK_OPTION){
            if(jList1.getSelectedIndex()==-1){
                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCaseConfig.this,
                                        "Error", "Please select one view!");
                return "";
            }
            String view = jList1.getSelectedValue().toString();
            if(tf!=null)tf.setText(view);
            return view;
        }
        return "";
    }
}




