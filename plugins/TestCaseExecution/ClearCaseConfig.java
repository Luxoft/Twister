/*
File: ClearCaseConfig.java ; This file is part of Twister.
Version: 2.003

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
                   jLabel8,jLabel9;
    private JPanel jPanel1,jPanel2,jPanel3,
                   jPanel4,jPanel6,jPanel7;
    private JButton libbtn,predefbtn,usrsutbtn,cfgbtn,
                    tcbtn,save,projbtn;
    private JTextField libpath,predefpath,predefview,
                       tcpath,tcview,cfgview,cfgpath,projpath,
                       usrsutpath,usrsutview,libview,projview;
    private JCheckBox tcactive,predefactive,projactive,libactive,usrsutactive,cfgactive;
    private JComboBox type;
    public ArrayList change;//array to hold items that change based on type
    private ClearCase cc;
    
    public ClearCaseConfig(Object[] addtochange, ClearCase cc){
        this.cc = cc;
        initComponents(addtochange);
        interpretConfig((Element)getRemoteConfigContent().getFirstChild());
    }
    
    
    private void initComponents(Object[] addtochange) {        
        main = new JPanel();
        add(main);
        jPanel1 = new JPanel();
        jLabel1 = new JLabel();
        jLabel2 = new JLabel();
        projpath = new JTextField();
        projview = new JTextField();
        projactive = new JCheckBox();
        projbtn = new JButton();
        jLabel3 = new JLabel();
        type = new JComboBox();
        jPanel3 = new JPanel();
        jLabel6 = new JLabel();
        jLabel7 = new JLabel();
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
        usrsutpath = new JTextField();
        usrsutview = new JTextField();
        usrsutactive = new JCheckBox();
        usrsutbtn = new JButton();
        save = new JButton();
        change = new ArrayList();
        for(Object ob:addtochange){
            change.add(ob);
        }
        jPanel1.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Projects Path"));

        jLabel1.setText("Path:");

        jLabel2.setText("View:");
        change.add(jLabel2);
        projactive.setText("Active:         ");
        projactive.setAlignmentY(0.0F);
        projactive.setBorder(null);
        projactive.setHorizontalTextPosition(SwingConstants.LEFT);

        projbtn.setText("List Views");
        projbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(projview);
            }
        });
        
        change.add(projbtn);
        GroupLayout jPanel1Layout = new GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel1)
                            .addComponent(jLabel2))
                        .addGap(18, 18, 18)
                        .addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(projpath)
                            .addGroup(jPanel1Layout.createSequentialGroup()
                                .addComponent(projview)
                                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(projbtn))))
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(projactive, GroupLayout.PREFERRED_SIZE, 115, GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 0, Short.MAX_VALUE)))
                .addContainerGap())
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addGap(5, 5, 5)
                .addComponent(projactive)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel1)
                    .addComponent(projpath, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(3, 3, 3)
                .addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel2)
                    .addComponent(projview, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(projbtn))
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        jPanel1Layout.linkSize(SwingConstants.VERTICAL, new Component[] {jLabel1, jLabel2, projactive, projbtn, projpath, projview});

        jLabel3.setText("Type:");

        type.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Base", "UCM" }));

        jPanel3.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Predefined Suites Path"));

        jLabel6.setText("Path:");

        jLabel7.setText("View:");
        change.add(jLabel7);
        predefactive.setText("Active:         ");
        predefactive.setAlignmentY(0.0F);
        predefactive.setBorder(null);
        predefactive.setHorizontalTextPosition(SwingConstants.LEFT);

        predefbtn.setText("List Views");
        predefbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(predefview);
            }
        });
        change.add(predefbtn);
        GroupLayout jPanel3Layout = new GroupLayout(jPanel3);
        jPanel3.setLayout(jPanel3Layout);
        jPanel3Layout.setHorizontalGroup(
            jPanel3Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel3Layout.createSequentialGroup()
                .addGroup(jPanel3Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel3Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel3Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel6)
                            .addComponent(jLabel7))
                        .addGap(18, 18, 18)
                        .addGroup(jPanel3Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(predefpath)
                            .addGroup(jPanel3Layout.createSequentialGroup()
                                .addComponent(predefview, GroupLayout.DEFAULT_SIZE, 474, Short.MAX_VALUE)
                                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(predefbtn))))
                    .addGroup(jPanel3Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(predefactive, GroupLayout.PREFERRED_SIZE, 115, GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 524, Short.MAX_VALUE)))
                .addContainerGap())
        );
        jPanel3Layout.setVerticalGroup(
            jPanel3Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel3Layout.createSequentialGroup()
                .addGap(5, 5, 5)
                .addComponent(predefactive)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel3Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel6)
                    .addComponent(predefpath, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(3, 3, 3)
                .addGroup(jPanel3Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel7)
                    .addComponent(predefview, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(predefbtn))
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        jPanel3Layout.linkSize(SwingConstants.VERTICAL, new Component[] {jLabel6, jLabel7, predefactive, predefbtn, predefpath, predefview});

        jPanel2.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Library Path"));

        jLabel4.setText("Path:");

        jLabel5.setText("View:");
        change.add(jLabel5);
        libactive.setText("Active:         ");
        libactive.setAlignmentY(0.0F);
        libactive.setBorder(null);
        libactive.setHorizontalTextPosition(SwingConstants.LEFT);

        libbtn.setText("List Views");
        libbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(libview);
            }
        });
        change.add(libbtn);
        GroupLayout jPanel2Layout = new GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addGroup(jPanel2Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel2Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel4)
                            .addComponent(jLabel5))
                        .addGap(18, 18, 18)
                        .addGroup(jPanel2Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(libpath)
                            .addGroup(jPanel2Layout.createSequentialGroup()
                                .addComponent(libview, GroupLayout.DEFAULT_SIZE, 474, Short.MAX_VALUE)
                                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(libbtn))))
                    .addGroup(jPanel2Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(libactive, GroupLayout.PREFERRED_SIZE, 115, GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 524, Short.MAX_VALUE)))
                .addContainerGap())
        );
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addGap(5, 5, 5)
                .addComponent(libactive)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel2Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel4)
                    .addComponent(libpath, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(3, 3, 3)
                .addGroup(jPanel2Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel5)
                    .addComponent(libview, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(libbtn))
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        jPanel2Layout.linkSize(SwingConstants.VERTICAL, new Component[] {jLabel4, jLabel5, libactive, libbtn, libpath, libview});

        jPanel4.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "TestCase Source Path"));

        jLabel8.setText("Path:");

        jLabel9.setText("View:");
        change.add(jLabel9);
        tcactive.setText("Active:         ");
        tcactive.setAlignmentY(0.0F);
        tcactive.setBorder(null);
        tcactive.setHorizontalTextPosition(SwingConstants.LEFT);

        tcbtn.setText("List Views");
        tcbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(tcview);
            }
        });
        change.add(tcbtn);
        GroupLayout jPanel4Layout = new GroupLayout(jPanel4);
        jPanel4.setLayout(jPanel4Layout);
        jPanel4Layout.setHorizontalGroup(
            jPanel4Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel4Layout.createSequentialGroup()
                .addGroup(jPanel4Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel4Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel4Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel8)
                            .addComponent(jLabel9))
                        .addGap(18, 18, 18)
                        .addGroup(jPanel4Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(tcpath)
                            .addGroup(jPanel4Layout.createSequentialGroup()
                                .addComponent(tcview, GroupLayout.DEFAULT_SIZE, 474, Short.MAX_VALUE)
                                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(tcbtn))))
                    .addGroup(jPanel4Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(tcactive, GroupLayout.PREFERRED_SIZE, 115, GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 524, Short.MAX_VALUE)))
                .addContainerGap())
        );
        jPanel4Layout.setVerticalGroup(
            jPanel4Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel4Layout.createSequentialGroup()
                .addGap(5, 5, 5)
                .addComponent(tcactive)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel4Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel8)
                    .addComponent(tcpath, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(3, 3, 3)
                .addGroup(jPanel4Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel9)
                    .addComponent(tcview, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(tcbtn))
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        jPanel4Layout.linkSize(SwingConstants.VERTICAL, new Component[] {jLabel8, jLabel9, tcactive, tcbtn, tcpath, tcview});

        jLabel10.setText("Path:");

        jLabel11.setText("View:");
        change.add(jLabel11);

        jPanel6.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Test Configuration Path"));

        jLabel12.setText("Path:");

        jLabel13.setText("View:");
        change.add(jLabel13);
        cfgactive.setText("Active:         ");
        cfgactive.setAlignmentY(0.0F);
        cfgactive.setBorder(null);
        cfgactive.setHorizontalTextPosition(SwingConstants.LEFT);

        cfgbtn.setText("List Views");
        cfgbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(cfgview);
            }
        });
        change.add(cfgbtn);
        GroupLayout jPanel6Layout = new GroupLayout(jPanel6);
        jPanel6.setLayout(jPanel6Layout);
        jPanel6Layout.setHorizontalGroup(
            jPanel6Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel6Layout.createSequentialGroup()
                .addGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel6Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel12)
                            .addComponent(jLabel13))
                        .addGap(18, 18, 18)
                        .addGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(cfgpath)
                            .addGroup(jPanel6Layout.createSequentialGroup()
                                .addComponent(cfgview, GroupLayout.DEFAULT_SIZE, 474, Short.MAX_VALUE)
                                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(cfgbtn))))
                    .addGroup(jPanel6Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(cfgactive, GroupLayout.PREFERRED_SIZE, 115, GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 524, Short.MAX_VALUE)))
                .addContainerGap())
        );
        jPanel6Layout.setVerticalGroup(
            jPanel6Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel6Layout.createSequentialGroup()
                .addGap(5, 5, 5)
                .addComponent(cfgactive)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel12)
                    .addComponent(cfgpath, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(3, 3, 3)
                .addGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel13)
                    .addComponent(cfgview, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(cfgbtn))
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        jPanel6Layout.linkSize(SwingConstants.VERTICAL, new Component[] {cfgactive, cfgbtn, cfgpath, cfgview, jLabel12, jLabel13});

        jPanel7.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "User SUT Files Path"));

        jLabel14.setText("Path:");

        jLabel15.setText("View:");
        change.add(jLabel15);
        usrsutactive.setText("Active:         ");
        usrsutactive.setAlignmentY(0.0F);
        usrsutactive.setBorder(null);
        usrsutactive.setHorizontalTextPosition(SwingConstants.LEFT);

        usrsutbtn.setText("List Views");
        usrsutbtn.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                listViews(usrsutview);
            }
        });
        change.add(usrsutbtn);
        GroupLayout jPanel7Layout = new GroupLayout(jPanel7);
        jPanel7.setLayout(jPanel7Layout);
        jPanel7Layout.setHorizontalGroup(
            jPanel7Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel7Layout.createSequentialGroup()
                .addGroup(jPanel7Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel7Layout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(jPanel7Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel14)
                            .addComponent(jLabel15))
                        .addGap(18, 18, 18)
                        .addGroup(jPanel7Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(usrsutpath)
                            .addGroup(jPanel7Layout.createSequentialGroup()
                                .addComponent(usrsutview, GroupLayout.DEFAULT_SIZE, 474, Short.MAX_VALUE)
                                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(usrsutbtn))))
                    .addGroup(jPanel7Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(usrsutactive, GroupLayout.PREFERRED_SIZE, 115, GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 524, Short.MAX_VALUE)))
                .addContainerGap())
        );
        jPanel7Layout.setVerticalGroup(
            jPanel7Layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(jPanel7Layout.createSequentialGroup()
                .addGap(5, 5, 5)
                .addComponent(usrsutactive)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel7Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel14)
                    .addComponent(usrsutpath, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(3, 3, 3)
                .addGroup(jPanel7Layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel15)
                    .addComponent(usrsutview, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(usrsutbtn))
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        jPanel7Layout.linkSize(SwingConstants.VERTICAL, new Component[] {jLabel14, jLabel15, usrsutbtn, usrsutactive, usrsutpath, usrsutview});

        save.setText("Save");

        GroupLayout layout = new GroupLayout(main);
        main.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jLabel3)
                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(type, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addComponent(jPanel1, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jPanel2, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jPanel3, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jPanel4, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jPanel6, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jPanel7, GroupLayout.Alignment.TRAILING, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addGroup(GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addGap(0, 0, Short.MAX_VALUE)
                        .addComponent(save)))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel3)
                    .addComponent(type, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel4, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel1, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel3, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel2, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel6, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel7, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(save)
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
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
                      for(Object ob:change){
                          if(ob instanceof JButton){
                              JButton but = (JButton)ob;
                              but.setText(but.getText().replace("Activitie","View"));
                          }else{
                              JLabel lab = (JLabel)ob;
                              lab.setText(lab.getText().replace("Activitie","View"));
                          }
                      }
                  } else {
                      for(Object ob:change){
                          if(ob instanceof JButton){
                              JButton but = (JButton)ob;
                              but.setText(but.getText().replace("View","Activitie"));
                          }else{
                              JLabel lab = (JLabel)ob;
                              lab.setText(lab.getText().replace("View","Activitie"));
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
        interpretTag(root.getElementsByTagName("TestCaseSourcePath").item(0),tcactive,tcview,tcpath);
        interpretTag(root.getElementsByTagName("UsersPath").item(0),projactive,projview,projpath);
        interpretTag(root.getElementsByTagName("PredefinedSuitesPath").item(0),predefactive,predefview,predefpath);
        interpretTag(root.getElementsByTagName("LibsPath").item(0),libactive,libview,libpath);
        interpretTag(root.getElementsByTagName("TestConfigPath").item(0),cfgactive,cfgview,cfgpath);
        interpretTag(root.getElementsByTagName("SutPath").item(0),usrsutactive,usrsutview,usrsutpath);
        try{String ttype = root.getElementsByTagName("Type").item(0).getAttributes().getNamedItem("type").getNodeValue();
            int size = type.getItemCount();
            for(int i = 0;i<size;i++){
                if(type.getItemAt(i).toString().equals(ttype)){
                    type.setSelectedIndex(i);
                    break;
                }
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
            try{addTag("TestCaseSourcePath",tcactive.isSelected(), tcview.getText(),tcpath.getText(),root,document);}
            catch(Exception e){addTag("TestCaseSourcePath",false,"","",root,document);}
            try{addTag("UsersPath",projactive.isSelected(), projview.getText(),projpath.getText(),root,document);}
            catch(Exception e){addTag("UsersPath",false,"","",root,document);}
            try{addTag("PredefinedSuitesPath",predefactive.isSelected(), predefview.getText(),predefpath.getText(),root,document);}
            catch(Exception e){addTag("PredefinedSuitesPath",false,"","",root,document);} 
            try{addTag("LibsPath",libactive.isSelected(), libview.getText(),libpath.getText(),root,document);}
            catch(Exception e){addTag("LibsPath",false,"","",root,document);}
            try{addTag("TestConfigPath",cfgactive.isSelected(), cfgview.getText(),cfgpath.getText(),root,document);}
            catch(Exception e){addTag("TestConfigPath",false,"","",root,document);}
            try{addTag("SutPath",usrsutactive.isSelected(), usrsutview.getText(),usrsutpath.getText(),root,document);}
            catch(Exception e){addTag("SutPath",false,"","",root,document);}
            Element rootElement = document.createElement("Type");
            rootElement.setAttribute("type",type.getSelectedItem().toString());
            root.appendChild(rootElement);
            File file = new File(RunnerRepository.temp+RunnerRepository.getBar()+
                                "Twister"+RunnerRepository.getBar()+"config"+RunnerRepository.getBar()+"clearcaseconfig.xml");
            Result result = new StreamResult(file);
            transformer.transform(source, result);
            FileInputStream in = new FileInputStream(file);
            RunnerRepository.uploadRemoteFile(RunnerRepository.USERHOME+"/twister/config/", in, "clearcaseconfig.xml",false,null);
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
    private void interpretTag(Node tag, JCheckBox check, JTextField view,JTextField path){
        try{String active = tag.getAttributes().getNamedItem("active").getNodeValue();
            String tview = tag.getAttributes().getNamedItem("view").getNodeValue();
            String tpath = tag.getAttributes().getNamedItem("path").getNodeValue();
            check.setSelected(Boolean.parseBoolean(active));
            view.setText(tview);
            path.setText(tpath);
        } catch(Exception e){
            System.out.println("Could not interpret "+tag.getNodeName()+" from clearcaseconfig.xml");
            e.printStackTrace();
        }
    }
    
    /*
     * create specifig tag used in config xml
     */
    private void addTag(String tagname, boolean active, String view, String path,
                              Element root,Document document){
        Element rootElement = document.createElement(tagname);
        rootElement.setAttribute("active",active+"");
        rootElement.setAttribute("view",view);
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
     * list views based on clearcase command
     * and assign selection to field
     */
    private void listViews(JTextField tf){
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
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,ClearCaseConfig.this,
                                        "Error", "Please select one view and input vob location");
                return ;
            }
            String view = jList1.getSelectedValue().toString();
            tf.setText(view);
            
        }
    }
}