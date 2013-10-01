/*
File: ClearCase.java ; This file is part of Twister.
Version: 2.004

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

import javax.swing.JTree;
import javax.swing.tree.MutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.DefaultMutableTreeNode;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import com.jcraft.jsch.JSchException;
import java.io.InputStream;
import java.io.PipedInputStream;
import java.io.PipedOutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import com.jcraft.jsch.ChannelExec;
import java.io.OutputStream;
import java.io.PrintStream;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JList;
import javax.swing.JLabel;
import javax.swing.JFrame;
import javax.swing.JTextArea;
import javax.swing.JCheckBox;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.ListSelectionModel;
import javax.swing.GroupLayout;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JOptionPane;
import javax.swing.JTextField;
import com.twister.CustomDialog;
import java.util.Vector;
import java.awt.Dimension;
import javax.swing.JComboBox;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;

public class ClearCase extends JPanel{
//     private DataInputStream dataIn;
//     private DataOutputStream dataOut;
    private BufferedReader in;
    private Channel channel;
    private boolean firstfind = false;
    private Session session;
    public String root="";
    public String view="";
    private PrintStream ps;
    private JLabel lview, vob;
    
    public ClearCase(String host, String user, String password){
        initializeSSH(host, user, password);
        initComponents();
    }
    
    private void initializeSSH(String host, String user, String password){
        try{JSch jsch = new JSch();
            session = jsch.getSession(user, host, 22);
            session.setPassword(password);
            session.setConfig("StrictHostKeyChecking", "no");
            session.connect();
            channel = session.openChannel("shell");
            channel.connect();
            in = new BufferedReader(new InputStreamReader(channel.getInputStream()));
            OutputStream ops = channel.getOutputStream();
            ps = new PrintStream(ops, false);
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    
//     public void sendCommand(String command,boolean endstring){
//         
//         try{if(endstring){
//                 command+=" ; echo @_#_";
//             }
//             ps.println(command); 
//             ps.flush();
//         } catch(Exception e){
//             e.printStackTrace();
//         }
//     }
    
    public void sendCommand(String command){
        try{
//             if(endstring){
//                 command+=" ; echo @_#_";
//             }
            command+=" ; echo @_#_";
            ps.println(command); 
            ps.flush();
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    
//     public String readOutput(boolean consume){
//         try{
//             if(consume){
//                 StringBuilder sb = new StringBuilder();
//                 String line = in.readLine();
//                 line = in.readLine();
//                 sb.append(line+"\n");
//                 System.out.println("line: "+line);
//                 line = in.readLine();
//                 sb.append(line+"\n");
//                 System.out.println("line: "+line);
//                 if(line.indexOf("No such")!=-1){
//                     line = in.readLine();
//                     sb.append(line+"\n");
//                     System.out.println("line: "+line);
//                     line = in.readLine();
//                     sb.append(line+"\n");
//                     System.out.println("line: "+line);
//                     return sb.toString();
//                 } else if(line.indexOf("Error")!=-1){
// //                     sb.append(line+"\n");
//                     while(line.indexOf("Error")!=-1){
//                         line = in.readLine();
//                         sb.append(line+"\n");
//                         System.out.println("line: "+line);
//                         line = in.readLine();
//                         sb.append(line+"\n");
//                         System.out.println("line: "+line);
//                     }
//                     return sb.toString();
//                 }
//                 System.out.println("line: "+line);
//                 System.out.println("line: "+in.readLine());
//                 return line;
//             }
//             else {
//                 String line = null;
//                 StringBuilder responseData = new StringBuilder();
//                 while((line = in.readLine()) != null) {
//                     System.out.println("line: "+line);
//                     responseData.append(line+"\n");
//                     if(line.indexOf("@_#_")!=-1){
//                         if(firstfind){
//                             firstfind = false;
//                             in.readLine();
//                             in.readLine();
//                             return responseData.substring(0, responseData.indexOf("@_#_")).toString();
//                         }
//                         else{
//                             responseData = new StringBuilder(responseData.substring(responseData.indexOf("@_#_")+4, responseData.length()));
//                             firstfind = true;
//                         }
//                     }
//                     else{
//                         if(line.indexOf("Error")!=-1){
//                             in.readLine();
//                             in.readLine();
//                             firstfind = false;
//                             return responseData.toString();
//                         }
//                     }
//                 }
//                 return responseData.toString();
//                 
//             
//             }
//             } catch(Exception e){
//                 e.printStackTrace();
//                 return null;
//             }
//     }

    public String readOutput(){
        try{
                String line = null;
                StringBuilder responseData = new StringBuilder();
                while((line = in.readLine()) != null) {
                    System.out.println("line: "+line);
                    responseData.append(line+"\n");
                    if(responseData.indexOf("cleartool: command not found")!=-1){
                        in.readLine();
                        in.readLine();
                        firstfind = false;
                        CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCase.this,
                                "ERROR", "ClearTool not installed!");
                        return null;
                    }
                    if(line.indexOf("@_#_")!=-1&&line.indexOf("echo")==-1){
                            in.readLine();
                            in.readLine();
                            if(responseData.indexOf("cleartool: command not found")!=-1){
                                CustomDialog.showInfo(JOptionPane.ERROR_MESSAGE,ClearCase.this,
                                        "ERROR", "ClearTool not installed!");
                                return null;
                            }
                            return responseData.substring(0, responseData.indexOf("@_#_")).toString();
                    } else if(line.indexOf("echo @_#_")!=-1){
                        responseData = new StringBuilder(responseData.substring(responseData.indexOf("@_#_")+4, responseData.length()));
                    }
                }
                return responseData.toString();
            } catch(Exception e){
                e.printStackTrace();
                return null;
            }
    }
    
    public void disconnect(){
        try{in.close();}
        catch(Exception e){e.printStackTrace();}
        try{ps.close();}
        catch(Exception e){e.printStackTrace();}
        channel.disconnect();
        session.disconnect();
    }
    
    private void initComponents() {
        JPanel jPanel1 = new JPanel();
        JButton listviews = new JButton("List Views");
        JLabel views = new JLabel();
        JScrollPane jScrollPane2 = new JScrollPane();
        final JTextArea tviews = new JTextArea();
        tviews.setEditable(false);
        final JCheckBox cshort = new JCheckBox();
        final JCheckBox clong = new JCheckBox();
        JButton setview = new JButton("Set View");
//         JButton endview = new JButton("End View");
        JButton showconf = new JButton("Show Config Spec");
        JButton mkelem = new JButton("Make Element");
        JButton rmelem = new JButton("Remove Element");
        JButton mklabel = new JButton("Make Label");
        JButton mkview = new JButton("Make View");
        lview = new JLabel();
        vob = new JLabel();
        
        mklabel.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
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
                
                JCheckBox recursive = new JCheckBox("Recursive");
                recursive.setBounds(10,250,100,25);
                p.add(recursive);
                
                int resp = (Integer)CustomDialog.showDialog(p,JOptionPane.PLAIN_MESSAGE,
                                                        JOptionPane.OK_CANCEL_OPTION, 
                                                        RunnerRepository.window, "Remove Element",
                                                        null);
                if(resp == JOptionPane.OK_OPTION){
                    String ulabel = tlabel.getText();
                    String ucomment = tcomment.getText();
                    String uelement = telement.getText();
                    String urecursive = "";
                    if(recursive.isSelected())urecursive = " -r ";
                    String uversion="";
                    if(!tversion.getText().equals(""))uversion = " -version "+tversion.getText()+" ";
                    sendCommand("cleartool mklabel "+urecursive+uversion+" -c \""+ucomment+"\" "+ulabel+" "+uelement);
                    String response = readOutput();
                    System.out.println(response);
                    tviews.setText(response);
                }
        }});
        
        rmelem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
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
                    String ucomment = tcomment.getText();
                    sendCommand("cleartool rmelem -f -c "+ucomment+" "+uelement);
                    String response = readOutput();
                    System.out.println(response);
                    tviews.setText(response);
                }
            }
        });
        
        mkelem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
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
                    String ucomment = tcomment.getText();
                    String utype = teltype.getText();
//                     sendCommand("newgrp neptune");
//                     try{System.out.println(in.readLine());
//                         System.out.println(in.readLine());
//                         System.out.println(in.readLine());
//                         System.out.println(in.readLine());
//                     } catch (Exception e){
//                         e.printStackTrace();
//                     }
//                     System.out.println(readOutput());
//                     sendCommand("cleartool setview bogdan_twister");
//                     try{System.out.println(in.readLine());
//                         System.out.println(in.readLine());
//                         System.out.println(in.readLine());
//                         System.out.println(in.readLine());
//                     } catch (Exception e){
//                         e.printStackTrace();
//                     }
                    //System.out.println(readOutput());
                    sendCommand("cleartool mkelem -c "+ucomment+" -eltype "+utype+" "+uelement);
                    String response = readOutput();
                    System.out.println(response);
                    tviews.setText(response);
                }
            }});
        
//         endview.addActionListener(new ActionListener(){
//             public void actionPerformed(ActionEvent ev){
//                 sendCommand("cleartool endview "+view,false);
//                 readOutput(true);
//                 lview.setText("");
//                 vob.setText("");
//                 view = "";
//                 root = "";
//             }
//         });
        mkview.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
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
                
                JCheckBox shareable = new JCheckBox("Shareable");
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
                    sendCommand(sb.toString());
                    String response = readOutput();
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
                if(view.equals("")){
                    CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,ClearCase.this,
                                        "Warning", "Please set view!");
                    return;
                }
                sendCommand("cleartool catcs -tag "+view);
                String content = readOutput();
                tviews.setText(content);
            }
        });

        listviews.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                String command = "cleartool lsview";
                if(cshort.isSelected()){
                    command+=" -short";
                } else if(clong.isSelected()){
                    command+=" -long";
                }
                sendCommand(command);
                tviews.setText(readOutput());
            }
        });
        setview.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                sendCommand("cleartool lsview -short");
                String [] resp = readOutput().split("\n");
                showViews(resp);
            }
        });
        views.setText("Views:");
        tviews.setColumns(20);
        tviews.setRows(5);
        jScrollPane2.setViewportView(tviews);
        cshort.setText("Short");
        cshort.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(cshort.isSelected()){
                    clong.setSelected(false);
                }
                System.out.println("selected");
            }
        });
        clong.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(clong.isSelected()){
                    cshort.setSelected(false);
                }
                System.out.println("selected");
            }
        });
        clong.setText("Long");
        setview.setText("Set View");
        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
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
                            .addComponent(showconf, javax.swing.GroupLayout.PREFERRED_SIZE, 140, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addComponent(listviews, javax.swing.GroupLayout.PREFERRED_SIZE, 100, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addContainerGap())
        );

        jPanel1Layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {listviews,setview,mkview,mkelem,rmelem,mklabel,showconf});

        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
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
                .addComponent(showconf)
                .addContainerGap(144, Short.MAX_VALUE))
        );

        lview.setText("View:");

        vob.setText("Vob:");

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 475, Short.MAX_VALUE)
                    .addComponent(vob, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(lview, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(4, 4, 4)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(lview)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(vob)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jScrollPane2))
                    .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap())
        );

//         javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
//         this.setLayout(layout);
//         layout.setHorizontalGroup(
//             layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
//                     .addGroup(layout.createSequentialGroup()
//                         .addComponent(cshort)
//                         .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                         .addComponent(clong))
//                     .addComponent(listviews, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
//                     .addComponent(setview, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
//                 .addGap(18, 18, 18)
//                 .addComponent(views)
//                 .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                 .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 467, Short.MAX_VALUE)
//                 .addContainerGap())
//         );
//         layout.setVerticalGroup(
//             layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//             .addGroup(layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
//                     .addComponent(jScrollPane2)
//                     .addGroup(layout.createSequentialGroup()
//                         .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                             .addComponent(listviews)
//                             .addComponent(views))
//                         .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
//                         .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
//                             .addComponent(cshort)
//                             .addComponent(clong))
//                         .addGap(18, 18, 18)
//                         .addComponent(setview)
//                         .addGap(0, 189, Short.MAX_VALUE)))
//                 .addContainerGap())
//         );
    }
    
    public void showViews(String [] views){
        JPanel libraries = new JPanel();
        JLabel jLabel1 = new JLabel();
        JTextField jTextField1 = new JTextField();
        JScrollPane jScrollPane1 = new JScrollPane();
        JList jList1 = new JList();
        jLabel1.setText("VOB Path:");
        jScrollPane1.setViewportView(jList1);
        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(libraries);
        libraries.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
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
                .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 247, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel1)
                    .addComponent(jTextField1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap())
        );
        jList1.setModel(new DefaultComboBoxModel(views));
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
//             sendCommand("cleartool setview "+view,false);
//             readOutput(true);
            sendCommand("cleartool setview "+view);
            try{String line = in.readLine();
                System.out.println("line: "+line);
                line = in.readLine();
                System.out.println("line: "+line);
                if(line.indexOf("Error")!=-1){
                    line = in.readLine();
                    System.out.println("line: "+line);
                    line = in.readLine();
                    System.out.println("line: "+line);
                }
            } catch (Exception e){
                e.printStackTrace();
            }
            
//             readOutput();
            root = jTextField1.getText();
//             sendCommand("cd  "+jTextField1.getText(),false);
//             readOutput(true);
            sendCommand("cd  "+jTextField1.getText());
            readOutput();
            RunnerRepository.window.mainpanel.p1.cp.refreshStructure();
            lview.setText("View: "+view);
            vob.setText("View: "+root);
        }
    }
    
    public void buildTree(DefaultMutableTreeNode node){
//         sendCommand("cleartool pwd",true);
//         String curentdir = readOutput(true);
        sendCommand("cleartool pwd");
        String curentdir = readOutput();
        curentdir = curentdir.substring(2, curentdir.length()-1);
        DefaultMutableTreeNode child = new DefaultMutableTreeNode(curentdir,true);
        node.add(child);
        Vector<String> folders = new Vector<String>();
        Vector<String> files = new Vector<String>();
        boolean directory = false;
        int firstindex,lastindex;
//         sendCommand("cleartool ls -l",true);
//         String [] lines = readOutput(false).split("\n");
        sendCommand("cleartool ls -l");
        String [] lines = readOutput().split("\n");
        for(String line:lines){
            if(line.indexOf("directory")==-1){
                directory = false;
            } else {
                directory = true;
            }
            if(line.indexOf("version")==-1)continue;
            firstindex = line.indexOf("version")+7; 
            lastindex = line.indexOf("@@"); 
            line = line.substring(firstindex, lastindex);
            for(int i=0;i<line.length();i++){
                if(line.charAt(i)!=' '){
                    line = line.substring(i);
                    break;
                }
            }
            if(directory){
                folders.add(line);
            } else {
                files.add(line);
            }
        }
        for(String folder:folders){
            System.out.println("folder: "+folder);
        }
        for(String file:files){
            System.out.println("file: "+file);
        }
        for(String folder:folders){
//             sendCommand("cd  "+curentdir+"/"+folder,false);
//             readOutput(true);
            sendCommand("cd  "+curentdir+"/"+folder);
            readOutput();
            buildTree(child);
//             sendCommand("cd  "+curentdir,false);
//             readOutput(true);
            sendCommand("cd  "+curentdir);
            readOutput();
        }
        for(String file:files){
            DefaultMutableTreeNode child2 = new DefaultMutableTreeNode(file,false);
            child.add(child2);
        }

    }
    
    
    public static void main(){
        try{ClearCase cc = new ClearCase("11.126.32.21","bpopescu","ina_1974CNP");
            JFrame f = new JFrame();
            f.setBounds(100, 100, 800, 600);
            f.setVisible(true);
            f.add(cc);
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}
