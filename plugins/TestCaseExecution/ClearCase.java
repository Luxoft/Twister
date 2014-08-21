/*
File: ClearCase.java ; This file is part of Twister.
Version: 3.025

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


import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.MouseInfo;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.io.BufferedReader;
import java.io.PrintStream;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import javax.swing.DefaultComboBoxModel;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JTabbedPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.tree.DefaultMutableTreeNode;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.twister.CustomDialog;

import java.awt.Color;

public class ClearCase extends JPanel{
    private BufferedReader in;
    private boolean firstfind = false;
    public String root="";
    private static String view="";
    private PrintStream ps;
    private JLabel lview, vob, lactivity,activity;
    private JButton showconf,mkelem,rmelem,mklabel,mkattr,mkview,
                    vdescribe,setactivity,unsetactivity,adescribe,listactivities;
    private String prompt = "twister_prompt#";
    private String shell;
    private String selectedactivity = "";
    private JPanel clearcasecmd;
//     private int BASE = 0;
    private String selectedtype = "Base";
    private ClearCaseConfig conf;
    private JCheckBox ashort,along;
    private JTextArea tactivity, tviews;
    
    
    public static void setView(String view){
        ClearCase.view = view;
    }
    
    public static String getView(){
        return ClearCase.view;
    }   
    
    
    public ClearCase(String host, String user, String password){
        initComponents();
    }

    /*
     * send command through ssh to server
     */
    public String sendCommand(HashMap<String, String> hash, boolean withoutprogressbar){
        JFrame progress = null;
        if(!withoutprogressbar){
            progress = new JFrame();
            JProgressBar bar = new JProgressBar();
            bar.setIndeterminate(true);
            progress.setAlwaysOnTop(true);
            progress.setLocation(MouseInfo.getPointerInfo().getLocation());
            progress.setUndecorated(true);
            progress.add(bar);
            progress.pack();
            progress.setVisible(true);   
        }
        try{
            System.out.println("Sending command: "+hash.toString());
            String result = RunnerRepository.getRPCClient().execute("run_plugin", new Object[]{RunnerRepository.user,
                                                                     "ClearCase",hash}).toString();
            System.out.println("respons: "+result);
            if(!withoutprogressbar)progress.dispose();
            if(result.length()>0&&result.charAt(0)=='\"')result = result.substring(1,result.length()-1);
            result = result.replaceAll("\\\\n", "\n");
            return result;
        } catch(Exception e){
            if(!withoutprogressbar)progress.dispose();
            System.out.println("Could not send command: "+hash.toString());
            e.printStackTrace();
            return "";
        }
    }
    
    
    private void initComponents() {
        
        JPanel ucmpanel = new JPanel();
        listactivities = new JButton("List Activities");
        
        listactivities.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                    new Thread(){
                        public void run(){
//                             tfilter.setText(RunnerRepository.user);
                            HashMap<String, String> hash = new HashMap<String, String>();
//                             if(conf.getType()!=BASE){
//                                 String view = conf.listViews(null);
//                                 String view = selectedview;
                                if(!view.equals("")){
                                    String command = "cleartool lsactivity";
                                    if(ashort.isSelected()){
                                        command+=" -short";
                                    } else if(along.isSelected()){
                                        command+=" -long";
                                    }
                                    hash.put("view", view);
                                    hash.put("command", command);
                                } else {
                                    CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCase.this,"Error", "No view selected");
                                    return;
                                }
                            String resp = sendCommand(hash,false);
//                             if(conf.getType()!=BASE){
//                                 resp = "one\ntwo\nthree\nfour";
//                             }
                            if(resp.indexOf("*ERROR*")!=-1){
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCase.this,"Error", resp);
                                return;
                            }
                            tactivity.setText(resp);
                        }
                    }.start();
            }
        });
        
        listactivities.setEnabled(false);
        ashort = new JCheckBox();
        ashort.setEnabled(false);
        along = new JCheckBox();
        along.setEnabled(false);
        ashort.setText("Short");
        ashort.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(ashort.isSelected()){
                    along.setSelected(false);
                }
            }
        });
        along.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(along.isSelected()){
                    ashort.setSelected(false);
                }
            }
        });
        along.setText("Long");        
        setactivity = new JButton("Set Activity");
        setactivity.setEnabled(false);
        
        
        
        
        setactivity.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                    new Thread(){
                        public void run(){
                                if(view.equals(""))return;
                                HashMap<String, String> hash = new HashMap<String, String>();
                                hash.put("view", view);
                                hash.put("command", "lsactivity");
                                String resp = sendCommand(hash,false).toString();
                                if(resp.indexOf("*ERROR*")!=-1){
                                    CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCase.this,
                                                                "Error", resp);
                                    return ;
                                }
                                String [] activities = resp.split("\n");
                                showActivities(activities,view);
                        }
                    }.start();
            }
        });
        
        
        
        
        unsetactivity = new JButton("Unset Activity");
        
        
        unsetactivity.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                    new Thread(){
                        public void run(){
                            HashMap<String, String> hash = new HashMap<String, String>();
                            hash.put("view", view);
                            hash.put("command", "cleartool setactivity -none");
                            String resp = sendCommand(hash,false);
                            tactivity.setText(resp);
//                             root = "";
//                             RunnerRepository.window.mainpanel.p1.cp.refreshStructure();
//                             vob.setText("Path: "+root);
//                             lactivity.setText("Activity: ");
                            activity.setText("Activity: ");
                            selectedactivity = "";
                            unsetactivity.setEnabled(false);
                            adescribe.setEnabled(false);
                        }
                    }.start();
            }
        });
        
        unsetactivity.setEnabled(false);
        adescribe = new JButton("Describe");
        
        
        
        adescribe.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                    StringBuilder sb = new StringBuilder();
                    sb.append("cleartool describe -cact");
                    HashMap<String, String> hash = new HashMap<String, String>();
                    hash.put("command", sb.toString());
                    String response = sendCommand(hash,false);
                    tactivity.setText(response);
        }});
        
        adescribe.setEnabled(false);        
        tactivity = new JTextArea();        
        activity = new JLabel("Activity: ");
        
        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(ucmpanel);
        ucmpanel.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(ashort)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(along))
                    .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(setactivity, javax.swing.GroupLayout.PREFERRED_SIZE, 100, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(unsetactivity, javax.swing.GroupLayout.PREFERRED_SIZE, 119, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(adescribe, javax.swing.GroupLayout.PREFERRED_SIZE, 140, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addComponent(listactivities, javax.swing.GroupLayout.PREFERRED_SIZE, 100, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addContainerGap())
        );
        
        jPanel1Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {listactivities, adescribe, unsetactivity, setactivity});

        jPanel1Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {listactivities, adescribe, unsetactivity, setactivity});

        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(listactivities)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(ashort)
                    .addComponent(along))
                .addGap(7, 7, 7)
                .addComponent(setactivity)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(unsetactivity)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(adescribe)
                .addContainerGap(10, 15))
        );
        
        JComboBox type = new JComboBox();
        
        type.addItemListener(new ItemListener(){
            public void itemStateChanged(ItemEvent event) {
               if (event.getStateChange() == ItemEvent.SELECTED) {
                  Object item = event.getItem();
                  if(item.toString().equals("Base")){
                      selectedtype = "Base";
                      activateUCMPanel();
                  } else {
                      selectedtype = "UCM";
                      activateUCMPanel();
                  }
               }
            }       
        });
        
        
        type.setModel(new javax.swing.DefaultComboBoxModel(new String[] { "Base", "UCM" }));
        JLabel jLabel1 = new JLabel("Type: ");
        
        JPanel typepanel = new JPanel();
        typepanel.add(jLabel1);
        typepanel.add(type);
        
        JTabbedPane tabs = new JTabbedPane(); 
        setLayout(new BorderLayout());
        add(tabs, BorderLayout.CENTER);
        JButton listviews = new JButton("List Views");
        JButton setview = new JButton("Set View");
        conf = new ClearCaseConfig(this);
        clearcasecmd = new JPanel();
        tabs.addTab("Control", clearcasecmd);
        tabs.addTab("Configuration", new JScrollPane(conf));
        JPanel jPanel1 = new JPanel();
        showconf = new JButton("Show Config Spec");
        showconf.setEnabled(false);
        mkelem = new JButton("Make Element");
        mkelem.setEnabled(false);
        rmelem = new JButton("Remove Element");
        rmelem.setEnabled(false);
        mklabel = new JButton("Make Label");
        mklabel.setEnabled(false);
        mkattr = new JButton("Make Attribute");
        mkattr.setEnabled(false);
        mkview = new JButton("Make View");
        mkview.setEnabled(false);
        vdescribe = new JButton("Describe");
        vdescribe.setEnabled(false);
        final JButton refresh = new JButton("Refresh");
        final JTextField tfilter = new JTextField();
        tfilter.setEnabled(false);
        refresh.setEnabled(false);
        JLabel views = new JLabel();
        JLabel filter = new JLabel("Filter: ");
        lactivity = new JLabel("Activity: ");
        tfilter.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(ev.getKeyCode()==KeyEvent.VK_ENTER){
                    refresh.doClick();
                }
            }
        });
        
        JScrollPane jScrollPane3 = new JScrollPane();
        tactivity.setColumns(20);
        tactivity.setRows(5);
        jScrollPane3.setViewportView(tactivity);
        
        JScrollPane jScrollPane2 = new JScrollPane();
        tviews = new JTextArea();
        tviews.setEditable(false);
        final JCheckBox cshort = new JCheckBox();
        final JCheckBox clong = new JCheckBox();
        
        lview = new JLabel();
        vob = new JLabel();
        
        refresh.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                new Thread(){
                    public void run(){
                        String filter = tfilter.getText();
                        String resp = null;
                        String command = "";
//                         if(conf.getType()!=BASE){
//                         command = " cleartool lsactivity";
//                         } else {
                            command = " cleartool lsview";
                            if(cshort.isSelected()){
                                command+=" -short";
                            } else if(clong.isSelected()){
                                command+=" -long";
                            }
//                             
//                         }
                        
                        if(!filter.equals("")){
                            command+=" | grep "+filter;
                        }
                        HashMap<String, String> hash = new HashMap<String, String>();
                        hash.put("command", command);
                        resp = sendCommand(hash,false);
                        
                        tviews.setText(resp);
                    }
                }.start();
        }});
        
        mkattr.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                new Thread(){
                    public void run(){
                        refresh.setEnabled(false);
                        tfilter.setEnabled(false);
                        JPanel p = new JPanel();
                        p.setLayout(null);
                        p.setPreferredSize(new Dimension(350,240));
                        
                        JLabel attr = new JLabel("Attribute: ");
                        attr.setBounds(10,10,70,25);
                        JTextField tattr = new JTextField();
                        tattr.setBounds(70,10,100,25);
                        p.add(attr);
                        p.add(tattr);
                        
                        JLabel value = new JLabel("Value: ");
                        value.setBounds(185,10,70,25);
                        JTextField tvalue = new JTextField();
                        tvalue.setBounds(230,10,100,25);
                        p.add(value);
                        p.add(tvalue);
                        
                        JLabel el = new JLabel("Element: ");
                        el.setBounds(10,40,70,25);
                        JTextField tel = new JTextField();
                        tel.setBounds(70,40,260,25);
                        p.add(el);
                        p.add(tel);
                        
                        JLabel version = new JLabel("Version: ");
                        version.setBounds(10,70,70,25);
                        JTextField tversion = new JTextField();
                        tversion.setBounds(70,70,260,25);
                        p.add(version);
                        p.add(tversion);
                        
                        JLabel comment = new JLabel("Comment: ");
                        comment.setBounds(10,100,70,25);
                        JTextArea tcomment = new JTextArea();
                        JScrollPane sp = new JScrollPane(tcomment);
                        sp.setBounds(70,100,260,80);
                        p.add(comment);
                        p.add(sp);
                        
                        JLabel cf = new JLabel("Comment File: ");
                        cf.setBounds(10,185,90,25);
                        JTextField tcf = new JTextField();
                        tcf.setBounds(95,185,235,25);
                        p.add(cf);
                        p.add(tcf);
                        JCheckBox recursive = new JCheckBox("recursive");
                        recursive.setBounds(10,215,80,25);
                        p.add(recursive);
                        JCheckBox replace = new JCheckBox("replace");
                        replace.setBounds(95,215,80,25);
                        p.add(replace);
                        
                        int resp = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE,
                                                                JOptionPane.OK_CANCEL_OPTION, 
                                                                RunnerRepository.window, "Make Attribute",
                                                                null);
                        if(resp == JOptionPane.OK_OPTION){
                            StringBuilder sb = new StringBuilder();
                            sb.append("cleartool mkattr ");
                            if(!tcomment.getText().equals("")){
                                sb.append(" -c ");
                                sb.append(tcomment.getText());
                                sb.append(" ");
                            } else if(!tcf.getText().equals("")){
                                sb.append(" -cfi ");
                                sb.append(tcf.getText());
                                sb.append(" ");
                            } else {
                                sb.append(" -nc ");
                            }
                            
                            if(!tversion.getText().equals("")){
                                sb.append(" -ver ");
                                sb.append(tversion.getText());
                                sb.append(" ");
                            }
                            
                            if(recursive.isSelected()){
                                sb.append(" -r ");
                            }
                            
                            if(replace.isSelected()){
                                sb.append(" -rep ");
                            }
                            
                            sb.append(tattr.getText());
                            sb.append(" ");
                            sb.append(tvalue.getText());
                            sb.append(" ");
                            sb.append(tel.getText());
                            HashMap<String, String> hash = new HashMap<String, String>();
                            hash.put("command", sb.toString());
                            tviews.setText(sendCommand(hash,false));
                        }
                    }}.start();
        }});
        
        vdescribe.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                refresh.setEnabled(false);
                tfilter.setEnabled(false);
                JPanel p = new JPanel();
                p.setLayout(null);
                p.setPreferredSize(new Dimension(350,200));
                
                final JTextField telement = new JTextField();
                final JTextField tcview = new JTextField();
                final JTextField thlink = new JTextField();
                final JTextField tlbtype = new JTextField();
                final JTextField tvob = new JTextField();
                
                JLabel element = new JLabel("Element: ");
                element.setBounds(10,10,70,25);
                telement.addFocusListener(new FocusAdapter(){
                    public void focusGained(FocusEvent ev){
//                         tcview.setText("");
//                         thlink.setText("");
//                         tvob.setText("");
//                         tlbtype.setText("");
                    }
                });
                telement.setBounds(90,10,250,25);
                p.add(element);
                p.add(telement);
                
                
                JLabel cview = new JLabel("Current View: ");
                cview.setBounds(10,40,80,25);
                tcview.addFocusListener(new FocusAdapter(){
                    public void focusGained(FocusEvent ev){
//                         telement.setText("");
//                         thlink.setText("");
//                         tvob.setText("");
//                         tlbtype.setText("");
                    }
                });
                tcview.setBounds(90,40,250,25);
                p.add(cview);
                p.add(tcview);
                
                JLabel hlink = new JLabel("HLink: ");
                hlink.setBounds(10,70,80,25);
                thlink.addFocusListener(new FocusAdapter(){
                    public void focusGained(FocusEvent ev){
//                         telement.setText("");
//                         tcview.setText("");
//                         tvob.setText("");
//                         tlbtype.setText("");
                    }
                });
                thlink.setBounds(90,70,250,25);
                p.add(hlink);
                p.add(thlink);
                
                JLabel lbtype = new JLabel("Label Type: ");
                lbtype.setBounds(10,100,80,25);
                tlbtype.addFocusListener(new FocusAdapter(){
                    public void focusGained(FocusEvent ev){
//                         telement.setText("");
//                         tcview.setText("");
//                         tvob.setText("");
//                         thlink.setText("");
                    }
                });
                tlbtype.setBounds(90,100,250,25);
                p.add(lbtype);
                p.add(tlbtype);
                
                JLabel vob = new JLabel("Path: ");
                vob.setBounds(10,130,80,25);
                tvob.addFocusListener(new FocusAdapter(){
                    public void focusGained(FocusEvent ev){
//                         telement.setText("");
//                         tcview.setText("");
//                         tlbtype.setText("");
//                         thlink.setText("");
                    }
                });
                tvob.setBounds(90,130,250,25);
                p.add(vob);
                p.add(tvob);
                
                final JCheckBox jlong = new JCheckBox("long");
                jlong.setBounds(10,160,55,25);
                final JCheckBox jshort = new JCheckBox("short");
                jshort.setBounds(65,160,55,25);
                final JCheckBox format = new JCheckBox("format");
                format.setBounds(120,160,65,25);
                final JTextField tformat = new JTextField();
                tformat.setEnabled(false);
                tformat.setBounds(185,160,155,25);
                p.add(jlong);
                p.add(jshort);
                p.add(format);
                p.add(tformat);
                
                jlong.addActionListener(new ActionListener(){
                    public void actionPerformed(ActionEvent ev){
                        if(jlong.isSelected()){
                            format.setSelected(false);
                            jshort.setSelected(false);
                            tformat.setEnabled(false);
                            tformat.setText("");
                        }
                    }
                });
                
                jshort.addActionListener(new ActionListener(){
                    public void actionPerformed(ActionEvent ev){
                        if(jshort.isSelected()){
                            jlong.setSelected(false);
                            format.setSelected(false);
                            tformat.setEnabled(false);
                            tformat.setText("");
                        }
                    }
                });
                
                format.addActionListener(new ActionListener(){
                    public void actionPerformed(ActionEvent ev){
                        if(format.isSelected()){
                            jlong.setSelected(false);
                            jshort.setSelected(false);
                            tformat.setEnabled(true);
                        }
                    }
                });
                
                
                int resp = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Describe",
                                                        null);
                if(resp == JOptionPane.OK_OPTION){
                    StringBuilder sb = new StringBuilder();
//                     if(conf.getType()!=BASE){ 
//                         sb.append("cleartool describe -cact");
//                     }else {
                        sb.append("cleartool describe ");
                        if(jlong.isSelected()){
                            sb.append(" -long ");
                        } else if (jshort.isSelected()){
                            sb.append(" -short ");
                        } else if(format.isSelected()){
                            sb.append(" -format \"");
                            sb.append(tformat.getText());
                            sb.append("\" ");
                        }
                        if(!telement.getText().equals("")){
                            sb.append(telement.getText());
                        } else if(!tcview.getText().equals("")){
                            sb.append(" -cview ");
                            sb.append(tcview.getText());
                        }else if(!thlink.getText().equals("")){
                            sb.append(" hlink:");
                            sb.append(thlink.getText());
                        }else if(!tlbtype.getText().equals("")){
                            sb.append(" lbtype:");
                            sb.append(tlbtype.getText());
                        }else if(!tvob.getText().equals("")){
                            sb.append(" vob:");
                            sb.append(tvob.getText());
                        }
//                     }
                    
                    HashMap<String, String> hash = new HashMap<String, String>();
                    hash.put("command", sb.toString());
                    String response = sendCommand(hash,false);
                    tviews.setText(response);
                }
        }});
        
        mklabel.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                refresh.setEnabled(false);
                tfilter.setEnabled(false);
                JPanel p = new JPanel();
                p.setLayout(null);
                p.setPreferredSize(new Dimension(350,280));
                JLabel label = new JLabel("Label: ");
                label.setBounds(10,10,70,25);
                JTextField tlabel = new JTextField();
                tlabel.setBounds(90,10,250,25);
                p.add(label);
                p.add(tlabel);
                
                JLabel element = new JLabel("Element: ");
                element.setBounds(10,40,70,25);
                JTextField telement = new JTextField();
                telement.setBounds(90,40,250,25);
                p.add(element);
                p.add(telement);
                
                JLabel version = new JLabel("Version: ");
                version.setBounds(10,70,70,25);
                JTextField tversion = new JTextField();
                tversion.setBounds(90,70,250,25);
                p.add(version);
                p.add(tversion);
                
                JLabel comment = new JLabel("Comment: ");
                comment.setBounds(10,100,70,25);
                JTextArea tcomment = new JTextArea();
                JScrollPane sp = new JScrollPane(tcomment);
                sp.setBounds(90,100,250,150);
                p.add(comment);
                p.add(sp);
                
                JCheckBox recursive = new JCheckBox("recursive");
                recursive.setBounds(10,250,100,25);
                p.add(recursive);
                
                int resp = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Remove Element",
                                                        null);
                if(resp == JOptionPane.OK_OPTION){
                    String ulabel = tlabel.getText();
                    String ucomment = " -c "+tcomment.getText();
                    if(tcomment.getText().equals(""))ucomment = " -nc ";
                    String uelement = telement.getText();
                    String urecursive = "";
                    if(recursive.isSelected())urecursive = " -recurse ";
                    String uversion="";
                    if(!tversion.getText().equals(""))uversion = " -version "+tversion.getText()+" ";
                    HashMap<String, String> hash = new HashMap<String, String>();
                    hash.put("command", "cleartool mklabel "+urecursive+uversion+ucomment+" "+ulabel+" "+uelement);
                    String response = sendCommand(hash,false);
                    tviews.setText(response);
                }
        }});
        
        rmelem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                refresh.setEnabled(false);
                tfilter.setEnabled(false);
                JPanel p = new JPanel();
                p.setLayout(null);
                p.setPreferredSize(new Dimension(350,200));
                JLabel element = new JLabel("Element: ");
                element.setBounds(10,10,70,25);
                JTextField telement = new JTextField();
                telement.setBounds(90,10,250,25);
                p.add(element);
                p.add(telement);
                
                JLabel comment = new JLabel("Comment: ");
                comment.setBounds(10,40,70,25);
                JTextArea tcomment = new JTextArea();
                JScrollPane sp = new JScrollPane(tcomment);
                sp.setBounds(90,40,250,150);
                p.add(comment);
                p.add(sp);
                
                int resp = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Remove Element",
                                                        null);
                if(resp == JOptionPane.OK_OPTION){
                    String uelement = telement.getText();
                    String ucomment = " -c "+tcomment.getText();
                    if(tcomment.equals(""))ucomment = " -nc ";
                    HashMap<String, String> hash = new HashMap<String, String>();
                    hash.put("command", "cleartool rmelem -f "+ucomment+" "+uelement);
                    String response = sendCommand(hash,false);
                    tviews.setText(response);
                }
            }
        });
        
        mkelem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                refresh.setEnabled(false);
                tfilter.setEnabled(false);
                JPanel p = new JPanel();
                p.setLayout(null);
                p.setPreferredSize(new Dimension(350,250));
                JLabel element = new JLabel("Element: ");
                element.setBounds(10,10,70,25);
                JTextField telement = new JTextField();
                telement.setBounds(90,10,250,25);
                p.add(element);
                p.add(telement);
                
                JLabel comment = new JLabel("Comment: ");
                comment.setBounds(10,40,70,25);
                JTextArea tcomment = new JTextArea();
                JScrollPane sp = new JScrollPane(tcomment);
                sp.setBounds(90,40,250,150);
                p.add(comment);
                p.add(sp);
                
                JLabel eltype = new JLabel("Element type: ");
                eltype.setBounds(10,195,80,25);
                final JTextField teltype = new JTextField("file");
                teltype.setEnabled(false);
                teltype.setBounds(220,195,120,25);
                JComboBox celtype = new JComboBox(new String[]{"file","compressed_file",
                                                               "text_file","compressed_text_file",
                                                               "binary_delta_file","html","ms_word",
                                                               "rose","rosert","xde","xml","directory ",
                                                               "file_system_object","user_defined"});
                celtype.addItemListener(new ItemListener(){
                    public void itemStateChanged(ItemEvent event) {
                        if (event.getStateChange() == ItemEvent.SELECTED) {
                            Object item = event.getItem();
                            if(item.toString().equals("user_defined")){
                                teltype.setEnabled(true);
                                teltype.setText("");
                                teltype.requestFocus();
                            } else {
                                teltype.setEnabled(false);
                                teltype.setText(item.toString());
                            }
                        }
                }});
                celtype.setBounds(90,195,125,25);
                
                p.add(eltype);
                p.add(celtype);
                p.add(teltype);
                
                int resp = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Make Element",
                                                        null);
                if(resp == JOptionPane.OK_OPTION){
                    String uelement = telement.getText();
                    String ucomment = " -c "+tcomment.getText();
                    if(tcomment.equals(""))ucomment = " -nc ";
                    String utype = teltype.getText();
                    HashMap<String, String> hash = new HashMap<String, String>();
                    hash.put("command", "cleartool mkelem "+ucomment+" -eltype "+utype+" "+uelement);
                    String response = sendCommand(hash,false);
                    tviews.setText(response);
                }
            }});
            
        mkview.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                refresh.setEnabled(false);
                tfilter.setEnabled(false);
                JPanel p = new JPanel();
                p.setLayout(null);
                p.setPreferredSize(new Dimension(300,250));
                JLabel tag = new JLabel("Tag:");
                JTextField ltag = new JTextField();
                tag.setBounds(10,10,50,25);
                ltag.setBounds(65,10,200,25);
                p.add(tag);
                p.add(ltag);
                JLabel view = new JLabel("View:");
                JTextField lview = new JTextField();
                view.setBounds(10,40,50,25);
                lview.setBounds(65,40,200,25);
                p.add(view);
                p.add(lview);
                JLabel region = new JLabel("Region:");
                JTextField lregion = new JTextField();
                region.setBounds(10,70,50,25);
                lregion.setBounds(65,70,200,25);
                p.add(region);
                p.add(lregion);
                
                JLabel host = new JLabel("Host:");
                JTextField lhost = new JTextField();
                host.setBounds(10,100,50,25);
                lhost.setBounds(65,100,200,25);
                p.add(host);
                p.add(lhost);
                JLabel hpath = new JLabel("HPath:");
                JTextField lhpath = new JTextField();
                hpath.setBounds(10,130,50,25);
                lhpath.setBounds(65,130,200,25);
                p.add(hpath);
                p.add(lhpath);
                JLabel gpath = new JLabel("GPath:");
                JTextField lgpath = new JTextField();
                gpath.setBounds(10,160,50,25);
                lgpath.setBounds(65,160,200,25);
                p.add(gpath);
                p.add(lgpath);
                
                JCheckBox shareable = new JCheckBox("shareable");
                shareable.setBounds(10,190,100,25);
                p.add(shareable);
                
                
                
                int resp = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Make View",
                                                        null);
                if(resp == JOptionPane.OK_OPTION){
                    if(ltag.getText().equals("")||lview.getText().equals("")){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,ClearCase.this,
                                        "Warning", "View and Tag are mandatory!");
                        return;
                    }
                    StringBuilder sb = new StringBuilder();
                    sb.append("cleartool mkview -tag ");
                    sb.append(ltag.getText());
                    if(!lregion.getText().equals("")){
                        sb.append(" -region "+lregion.getText());
                    }
                    if(!lhost.getText().equals("")){
                        sb.append(" -host "+lhost.getText());
                    }
                    if(!lhpath.getText().equals("")){
                        sb.append(" -hpath "+lhpath.getText());
                    }
                     if(!lgpath.getText().equals("")){
                        sb.append(" -gpath "+lgpath.getText());
                    }
                    if(shareable.isSelected()){
                        sb.append(" -shareable_dos ");
                    }
                    sb.append(" "+lview.getText());
                    System.out.println("Sending command: "+sb.toString());
                    HashMap<String, String> hash = new HashMap<String, String>();
                    hash.put("command", sb.toString());
                    String response = sendCommand(hash,false);
                    sb.setLength(0);
                    if(response.indexOf("Error")!=-1){
                        String[] lines = response.split("\n");
                        sb.append("<html>");
                        for(String l:lines){
                            sb.append(l);
                            sb.append("<br>");
                        }
                        sb.append("</html>");
                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCase.this,
                                              "ERROR", sb.toString());
                    }
                    tviews.setText(response);
                }
            }
        });
        showconf.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                new Thread(){
                    public void run(){
                        refresh.setEnabled(false);
                        tfilter.setEnabled(false);
                        if(view.equals("")){
                            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,ClearCase.this,
                                                "Warning", "Please set view!");
                            return;
                        }
                        HashMap<String, String> hash = new HashMap<String, String>();
                        hash.put("command", "cleartool catcs -tag "+view);
                        String content = sendCommand(hash,false);
                        tviews.setText(content);
                    }
                }.start();
            }
        });

        listviews.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                    new Thread(){
                        public void run(){
                            tfilter.setText(RunnerRepository.user);
                            HashMap<String, String> hash = new HashMap<String, String>();
//                             if(conf.getType()!=BASE){
//                                 String view = conf.listViews(null);
//                                 if(!view.equals("")){
//                                     hash.put("view", view);
//                                     hash.put("command", "lsactivity");
//                                 } else {
//                                     CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCase.this,"Error", "No view selected");
//                                     return;
//                                 }
//                             } else {
                                String command = "cleartool lsview";
                                if(cshort.isSelected()){
                                    command+=" -short";
                                } else if(clong.isSelected()){
                                    command+=" -long";
                                }
                                hash.put("command", command+" | grep "+RunnerRepository.user);
//                             }
                            
                            String resp = sendCommand(hash,false);
//                             if(conf.getType()!=BASE){
//                                 resp = "one\ntwo\nthree\nfour";
//                             }
                            if(resp.indexOf("*ERROR*")!=-1){
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCase.this,"Error", resp);
                                return;
                            }
                            tviews.setText(resp);
                            refresh.setEnabled(true);
                            tfilter.setEnabled(true);
                        }
                    }.start();
            }
        });
        setview.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                    new Thread(){
                        public void run(){
                            refresh.setEnabled(false);
                            tfilter.setEnabled(false);
//                             if(conf.getType()==BASE){
                            HashMap<String, String> hash = new HashMap<String, String>();
                            hash.put("command", " cleartool lsview -short | grep "+RunnerRepository.user);
                            String [] resp = sendCommand(hash,false).split("\n");
                            showViews(resp);
                        }
                    }.start();
            }
        });
        views.setText("Views:");
        tviews.setColumns(20);
        tviews.setRows(5);
        jScrollPane2.setViewportView(tviews);
        jScrollPane3.setViewportView(tactivity);
        cshort.setText("Short");
        cshort.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(cshort.isSelected()){
                    clong.setSelected(false);
                }
            }
        });
        clong.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(clong.isSelected()){
                    cshort.setSelected(false);
                }
            }
        });
        clong.setText("Long");
        jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addGap(10, 10, 10)
                        .addComponent(cshort)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(clong))
                    .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(setview, javax.swing.GroupLayout.PREFERRED_SIZE, 100, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(mkview, javax.swing.GroupLayout.PREFERRED_SIZE, 119, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(mkelem, javax.swing.GroupLayout.PREFERRED_SIZE, 119, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(rmelem, javax.swing.GroupLayout.PREFERRED_SIZE, 119, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(mklabel, javax.swing.GroupLayout.PREFERRED_SIZE, 119, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(mkattr, javax.swing.GroupLayout.PREFERRED_SIZE, 119, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(showconf, javax.swing.GroupLayout.PREFERRED_SIZE, 140, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(vdescribe, javax.swing.GroupLayout.PREFERRED_SIZE, 140, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addComponent(listviews, javax.swing.GroupLayout.PREFERRED_SIZE, 100, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addContainerGap())
        );
        
        jPanel1Layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {listviews, setview, mkview, mkelem, rmelem, mklabel, mkattr, showconf, vdescribe});

        jPanel1Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {listviews,setview,mkview,mkelem,rmelem,mklabel,mkattr,showconf,vdescribe});

        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(listviews)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(cshort)
                    .addComponent(clong))
                .addGap(7, 7, 7)
                .addComponent(setview)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(mkview)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(mkelem)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(rmelem)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(mklabel)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(mkattr)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(showconf)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(vdescribe)
                .addContainerGap(10,15)
                )
        );

        lview.setText("View:");

        vob.setText("Path:");
        
        
        
        

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(clearcasecmd);
        clearcasecmd.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addComponent(typepanel,javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(ucmpanel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 475, Short.MAX_VALUE)
                    .addComponent(vob, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
//                     .addComponent(lactivity, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(lview, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(filter)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(tfilter, javax.swing.GroupLayout.PREFERRED_SIZE, 149, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(refresh))
                    .addComponent(activity)
                    .addComponent(jScrollPane3,javax.swing.GroupLayout.DEFAULT_SIZE, 475, Short.MAX_VALUE)
                    .addGap(0, 0, Short.MAX_VALUE))
            .addContainerGap())
        );
                
                
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(4, 4, 4)
                .addComponent(typepanel,javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(lview)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(vob)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(filter)
                            .addComponent(tfilter, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(refresh))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 237, Short.MAX_VALUE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(activity)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(ucmpanel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                            .addComponent(jScrollPane3, javax.swing.GroupLayout.DEFAULT_SIZE, 237, Short.MAX_VALUE))
                        //.addComponent(jScrollPane3)
                        )
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        //.addComponent(ucmpanel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        )
                        )
                .addContainerGap()));
        
        layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {refresh, tfilter});
        
        layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {typepanel,jPanel1,ucmpanel});
        ClearCase.view = "";
    }
    
    //interprets the configuration and enables accordingly the ucm panel
    public void activateUCMPanel(){
        if(selectedtype.equals("UCM") && !view.equals("")){
            setactivity.setEnabled(true);
            if(!selectedactivity.equals("")){
                adescribe.setEnabled(true);
                unsetactivity.setEnabled(true);
            }
            ashort.setEnabled(true);
            along.setEnabled(true);
            listactivities.setEnabled(true);
        } else {
            setactivity.setEnabled(false);
            unsetactivity.setEnabled(false);
            ashort.setEnabled(false);
            along.setEnabled(false);
            adescribe.setEnabled(false);
            listactivities.setEnabled(false);
        }
    }
    
    
    /*
     * displays views and sets view
     * and vob on ClearCase server
     */
    public void showActivities(String [] activities,String view){
        JPanel libraries = new JPanel();
        JLabel jLabel1 = new JLabel();
//         JTextField jTextField1 = new JTextField();
        JScrollPane jScrollPane1 = new JScrollPane();
        final JList jList1 = new JList();
//         jLabel1.setText("VOB Path:");
        jScrollPane1.setViewportView(jList1);
        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(libraries);
        libraries.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jScrollPane1)
//                     .addGroup(layout.createSequentialGroup()
//                         .addComponent(jLabel1)
//                         .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
// //                         .addComponent(jTextField1, javax.swing.GroupLayout.DEFAULT_SIZE, 327, Short.MAX_VALUE)
//                         )
                        )
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 247, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
//                 .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                     .addComponent(jLabel1)
//                     .addComponent(jTextField1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap())
        );
        jList1.setModel(new DefaultComboBoxModel(activities));
        int resp = (Integer)CustomDialog.showDialog(libraries,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Activites",
                                                        null);
        if(resp == JOptionPane.OK_OPTION){
            if(jList1.getSelectedIndex()==-1){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,ClearCase.this,
                                        "Error", "Please select one activities");
                return ;
            }
            String activity = jList1.getSelectedValue().toString();
            HashMap<String, String> hash = new HashMap<String, String>();
            hash.put("view", view);
            hash.put("command", "cleartool setactivity "+activity);
            sendCommand(hash,false);
//             root = jTextField1.getText();
            RunnerRepository.window.mainpanel.p1.cp.refreshStructure();
//             vob.setText("Path: "+root);
//             lactivity.setText("Activity: "+activity);
            this.activity.setText("Activity: "+activity);
            selectedactivity = activity;
            unsetactivity.setEnabled(true);
            adescribe.setEnabled(true);
        }
    }
    
    /*
     * displays views and sets view
     * and vob on ClearCase server
     */
    public void showViews(String [] views){
        JPanel libraries = new JPanel();
        JLabel jLabel1 = new JLabel();
        JTextField jTextField1 = new JTextField();
        JScrollPane jScrollPane1 = new JScrollPane();
        final JList jList1 = new JList();
        JLabel filter = new JLabel("List View Filter:");
        final JTextField tfilter = new JTextField();
        tfilter.setText(RunnerRepository.user);
        JButton refresh = new JButton("Refresh");
        jLabel1.setText("VOB Path:");
        jScrollPane1.setViewportView(jList1);
        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(libraries);
        libraries.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(filter)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(tfilter, javax.swing.GroupLayout.PREFERRED_SIZE, 149, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(refresh)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addComponent(jScrollPane1)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jLabel1)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jTextField1, javax.swing.GroupLayout.DEFAULT_SIZE, 327, Short.MAX_VALUE)))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(filter)
                    .addComponent(tfilter, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(refresh))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 247, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel1)
                    .addComponent(jTextField1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap())
        );
        
        layout.linkSize(javax.swing.SwingConstants.VERTICAL, new java.awt.Component[] {refresh, tfilter});
        jList1.setModel(new DefaultComboBoxModel(views));
        
        refresh.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                new Thread(){
                    public void run(){
                       String filter = tfilter.getText();
                        String [] resp = null;
                        String command = "";
//                         if(conf.getType()!=BASE){
//                                 command = " cleartool lsactivity";
//                             if(!filter.equals("")){
//                                 command = " cleartool lsactivity | grep "+filter;
//                             }
//                         } else {
                            command = " cleartool lsview -short ";
                            if(!filter.equals("")){
                                command = " cleartool lsview -short | grep "+filter;
                            }
//                         }
                        HashMap<String, String> hash = new HashMap<String, String>();
                        hash.put("command", command);
                        resp = sendCommand(hash,false).split("\n");
                        jList1.setModel(new DefaultComboBoxModel(resp)); 
                    }
                }.start();
        }});
        
        int resp = (Integer)CustomDialog.showDialog(libraries,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Views",
                                                        null);
        if(resp == JOptionPane.OK_OPTION){
            if(jList1.getSelectedIndex()==-1||jTextField1.getText().equals("")){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,ClearCase.this,
                                        "Error", "Please select one view and input vob location");
                return ;
            }
            view = jList1.getSelectedValue().toString();
            HashMap<String, String> hash = new HashMap<String, String>();
            hash.put("command", "cleartool setview "+view);
            sendCommand(hash,false);
            root = jTextField1.getText();
            RunnerRepository.window.mainpanel.p1.cp.refreshStructure();
            lview.setText("View: "+view);
            vob.setText("Path: "+root);
            lactivity.setText("Activity: ");
            showconf.setEnabled(true);
            mkelem.setEnabled(true);
            rmelem.setEnabled(true);
            mklabel.setEnabled(true);
            mkattr.setEnabled(true);
            mkview.setEnabled(true);
            vdescribe.setEnabled(true);
            activateUCMPanel();
        }
    }
    
    /*
     * used to create ClearCase tc tree, calls
     * ClearCaseplugin and interprets the result
     */
    public void buildTree(DefaultMutableTreeNode node,JsonObject element){
        Iterator iter = element.entrySet().iterator();
        while(iter.hasNext()){
            Map.Entry entry = (Map.Entry)iter.next();
            if(!entry.getKey().equals("")){
                DefaultMutableTreeNode child2 = new DefaultMutableTreeNode(node+"/"+entry.getKey(),true);
                node.add(child2);
                JsonElement el = (JsonElement)entry.getValue();
                buildTree(child2,(JsonObject)el);
            }
        }
        JsonArray files = element.get("").getAsJsonArray();
        for(int i=0;i<files.size();i++){
            DefaultMutableTreeNode child2 = new DefaultMutableTreeNode(files.get(i).getAsString(),false);
            node.add(child2);
        }
    }
}