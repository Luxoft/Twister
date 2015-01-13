/*
File: Emails.java ; This file is part of Twister.
Version: 3.003

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
import java.awt.Dimension;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import java.awt.Font;
import javax.swing.border.TitledBorder;
import javax.swing.JTextArea;
import java.awt.Dimension;
import javax.swing.border.BevelBorder;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JScrollPane;
import java.awt.Color;
import javax.swing.JCheckBox;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import java.io.File;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import javax.swing.JPasswordField;
import javax.xml.transform.Result;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.dom.DOMSource;
import java.io.FileInputStream;
import javax.swing.JOptionPane;
import com.twister.CustomDialog;
import javax.xml.bind.DatatypeConverter;

public class Emails extends JPanel{
    public  JPanel p1;
    private JCheckBox check;
    private JTextField tipname, tport, tuser, tfrom;
    private JPasswordField tpass;
    private JTextArea emails, message, subject;
    private JLabel enable;
    private String initialpass;

    public Emails(){
        setLayout(null);
        setPreferredSize(new Dimension(450,560));
        setBackground(Color.WHITE);
        TitledBorder border = BorderFactory.createTitledBorder("SMTP server");
        border.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        JPanel p1 = new JPanel();
        p1.setBackground(Color.WHITE);
        p1.setBorder(border);         
        p1.setLayout(null);    
        p1.setBounds(80,80,350,70);
        JLabel ipname = new JLabel("IP/Name: ");
        ipname.setBounds(10,18,80,20);
        p1.add(ipname);
        tipname = new JTextField();
        tipname.setBounds(80,17,250,25);
        p1.add(tipname);
        JLabel port = new JLabel("Port: ");
        port.setBounds(10,40,80,20);
        p1.add(port);
        tport = new JTextField();
        tport.setBounds(80,40,250,25);
        p1.add(tport);
        add(p1);
        border = BorderFactory.createTitledBorder("Authentication");
        border.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        JPanel p2 = new JPanel();
        p2.setBackground(Color.WHITE);
        p2.setBorder(border);         
        p2.setLayout(null);    
        p2.setBounds(80,153,350,95);
        JLabel user = new JLabel("User: ");
        user.setBounds(10,18,80,20);
        p2.add(user);
        tuser = new JTextField();
        tuser.setBounds(80,17,250,25);
        p2.add(tuser);
        JLabel pass = new JLabel("Password: ");
        pass.setBounds(10,40,100,20);
        p2.add(pass);
        tpass = new JPasswordField();
        tpass.setBounds(80,40,250,25);
        p2.add(tpass);
        JLabel from = new JLabel("From: ");
        from.setBounds(10,63,80,20);
        p2.add(from);
        tfrom = new JTextField();
        tfrom.setBounds(80,63,250,25);
        p2.add(tfrom);
        add(p2);
        border = BorderFactory.createTitledBorder("Email List");
        border.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        JPanel p3 = new JPanel();
        p3.setBackground(Color.WHITE);
        p3.setBorder(border);         
        p3.setLayout(null);    
        p3.setBounds(80,251,350,68);
        emails = new JTextArea();
        emails.setLineWrap(true);
        emails.setWrapStyleWord(true);
        JScrollPane scroll = new JScrollPane(emails);
        scroll.setBounds(7,18,336,45);
        p3.add(scroll);        
        add(p3);
        border = BorderFactory.createTitledBorder("Subject");
        border.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        JPanel p5 = new JPanel();
        p5.setBackground(Color.WHITE);
        p5.setBorder(border);         
        p5.setLayout(null);    
        p5.setBounds(80,324,350,58);
        subject = new JTextArea();
        subject.setLineWrap(true);
        subject.setWrapStyleWord(true);
        JScrollPane scroll3 = new JScrollPane(subject);
        scroll3.setBounds(7,18,336,35);
        p5.add(scroll3);        
        add(p5);
        border = BorderFactory.createTitledBorder("Message");
        border.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        JPanel p4 = new JPanel();
        p4.setBackground(Color.WHITE);
        p4.setBorder(border);         
        p4.setLayout(null);    
        p4.setBounds(80,387,350,108);
        message = new JTextArea();
        message.setLineWrap(true);
        message.setWrapStyleWord(true);
        JScrollPane scroll2 = new JScrollPane(message);
        scroll2.setBounds(7,18,336,85);
        p4.add(scroll2);        
        add(p4);
        enable = new JLabel("Disabled");
        enable.setBounds(360,500,60,20);
        add(enable);

        check = new JCheckBox();
        check.setBounds(412,500,20,20);
        check.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(check.isSelected())enable.setText("Enabled");
                else enable.setText("Disabled");}});
        add(check);
        JButton save = new JButton("Save");
        if(!PermissionValidator.canEditEmail()){
            save.setEnabled(false);
        }
        save.setBounds(352,525,80,20);
        save.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                boolean saved = true;
                if(tpass.getPassword().length == 0){
                    CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Emails.this, "Warning", "Warning, password not set");}
                try{
                    File theone = new File(RunnerRepository.temp+RunnerRepository.getBar()+"Twister"+RunnerRepository.getBar()+"config"+RunnerRepository.getBar()+new File(RunnerRepository.REMOTEEMAILCONFIGFILE).getName());
                    DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
                    DocumentBuilder db = dbf.newDocumentBuilder();                                        
                    Document doc = db.parse(theone);
                    doc.getDocumentElement().normalize();
                    try{NodeList nodeLst = doc.getElementsByTagName("Enabled");
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(check.isSelected()+"");
                        else nodeLst.item(0).appendChild(doc.createTextNode(check.isSelected()+""));
                        nodeLst = doc.getElementsByTagName("SMTPPath");
                        String SMTPPath = tipname.getText()+":"+tport.getText();
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(SMTPPath);
                        else nodeLst.item(0).appendChild(doc.createTextNode(SMTPPath));
                        nodeLst = doc.getElementsByTagName("SMTPUser");
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(tuser.getText());
                        else nodeLst.item(0).appendChild(doc.createTextNode(tuser.getText()));
                        if( !(new String(tpass.getPassword()).equals("****"))){
                            nodeLst = doc.getElementsByTagName("SMTPPwd");
                            String p = new String(tpass.getPassword());
                            if(!initialpass.equals(p)){
                                try{p = RunnerRepository.getRPCClient().execute("encrypt_text", new Object[]{p}).toString();
                                    tpass.setText(p);
                                    initialpass = p;
                                } catch(Exception e){
                                    e.printStackTrace();
                                }
                            }
                            if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(p);
                            else nodeLst.item(0).appendChild(doc.createTextNode(p));}
                        nodeLst = doc.getElementsByTagName("From");
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(tfrom.getText());
                        else nodeLst.item(0).appendChild(doc.createTextNode(tfrom.getText()));
                        nodeLst = doc.getElementsByTagName("To");
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(emails.getText());
                        else nodeLst.item(0).appendChild(doc.createTextNode(emails.getText()));
                        nodeLst = doc.getElementsByTagName("Message");
                        if(message.getText().equals("")){
                            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,Emails.this,"Warning", "Message is empty");
                        }
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(message.getText());
                        else nodeLst.item(0).appendChild(doc.createTextNode(message.getText()));
                        nodeLst = doc.getElementsByTagName("Subject");
                        if(subject.getText().equals("")){
                            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,Emails.this,"Warning", "Subject is empty");
                        }
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(subject.getText());
                        else nodeLst.item(0).appendChild(doc.createTextNode(subject.getText()));}
                    catch(Exception e){
                        System.out.println(doc.getDocumentURI()+" may not be properly formatted");
                        saved = false;}
                    Result result = new StreamResult(theone); 
                    try{DOMSource source = new DOMSource(doc);
                        TransformerFactory transformerFactory = TransformerFactory.newInstance();
                        Transformer transformer = transformerFactory.newTransformer();
                        transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
                        transformer.setOutputProperty(OutputKeys.INDENT, "yes");
                        transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");                        
                        transformer.transform(source, result);  
                        FileInputStream input = new FileInputStream(theone);
                        saved = RunnerRepository.uploadRemoteFile(RunnerRepository.REMOTEEMAILCONFIGPATH,input,null,theone.getName(),false,null);
                    }
                    catch(Exception e){
                        e.printStackTrace();
                        System.out.println("Could not save in file : "+RunnerRepository.temp+RunnerRepository.getBar()+"Twister"+RunnerRepository.getBar()+"config"+RunnerRepository.getBar()+RunnerRepository.REMOTEEMAILCONFIGFILE+" and send to "+RunnerRepository.REMOTEEMAILCONFIGPATH);
                        saved = false;}}
                catch(Exception e){
                    e.printStackTrace();
                    saved = false;}
                if(saved)CustomDialog.showInfo(JOptionPane.INFORMATION_MESSAGE, Emails.this, "Successful", "File successfully saved");
                else CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, Emails.this, "Warning", "File could not be saved");}});
        add(save);
        JButton test = new JButton("Test");
        test.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                testEmail();
            }
        });
        test.setBounds(260,525,80,20);
        add(test);
    }
    
    private void testEmail(){
        try{
            String result = RunnerRepository.getRPCClient().execute("send_mail",
                            new Object[]{RunnerRepository.user,"true"}).toString();
            if(!result.equals("true")){
                CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,Emails.this,
                                        "Error", result);
            } else {
                CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE,Emails.this,
                                        "Success", "Email sent");
            }
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    
    public void setIPName(String ipname){
        tipname.setText(ipname);}
        
    public void setPassword(String password){
        tpass.setText(password);
        initialpass = password;
    }
    
    public void setPort(String port){
        tport.setText(port);}
        
    public void setUser(String user){
        tuser.setText(user);}
        
    public void setFrom(String from){
        tfrom.setText(from);}
        
    public void setEmails(String emails){
        this.emails.setText(emails);}
        
    public void setMessage(String message){
        this.message.setText(message);}
        
    public void setSubject(String subject){
        this.subject.setText(subject);}
        
    public void setCheck(boolean check){
        this.check.setSelected(check);
        if(check)enable.setText("Enabled");
        else enable.setText("Disabled");}}
