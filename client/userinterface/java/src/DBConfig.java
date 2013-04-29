/*
File: DBConfig.java ; This file is part of Twister.
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
import java.awt.Dimension;
import javax.swing.border.BevelBorder;
import javax.swing.BorderFactory;
import java.awt.Color;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.io.FileInputStream;
import java.io.File;
import java.nio.file.Files;
import static java.nio.file.StandardCopyOption.REPLACE_EXISTING;
import javax.swing.JPasswordField;
import java.io.InputStream;
import java.io.ByteArrayOutputStream;
import java.io.FileOutputStream;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.transform.Result;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.dom.DOMSource;
import javax.swing.JOptionPane;
import com.twister.CustomDialog;
import java.io.BufferedWriter;
import java.io.FileWriter;

public class DBConfig extends JPanel{
    Document doc=null;
    File theone;
    JTextField tdatabase,tserver,tuser;
    JPasswordField tpassword;

    public DBConfig(){
        setLayout(null);
        setPreferredSize(new Dimension(450,480));
        setBorder(BorderFactory.createBevelBorder(BevelBorder.LOWERED));
        setBackground(Color.WHITE);
        JLabel file = new JLabel("File: ");
        file.setBounds(15,10,50,20);
        add(file);
        final JTextField tfile = new JTextField();
        tfile.setBounds(100,10,170,25);
        add(tfile);
        JButton browse = new JButton("Browse");
        browse.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                JFileChooser chooser = new JFileChooser(); 
                chooser.setFileFilter(new XMLFilter());
                chooser.setCurrentDirectory(new java.io.File("."));
                chooser.setDialogTitle("Select XML File"); 
                if (chooser.showOpenDialog(Repository.window) == JFileChooser.APPROVE_OPTION) {                     
                    File f = chooser.getSelectedFile();
                    try{tfile.setText(f.getCanonicalPath());}
                    catch(Exception e){e.printStackTrace();}}}});
        browse.setBounds(275,13,90,20);
        add(browse);
        JButton upload = new JButton("Upload");
        upload.setBounds(375,13,90,20);
        upload.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                boolean saved = true;
                try{File f = new File(tfile.getText());
                    
//                     Repository.c.cd(Repository.REMOTEDATABASECONFIGPATH);
                    FileInputStream stream = new FileInputStream(f);
//                     Repository.c.put(stream,f.getName());
//                     stream.close();
                    
                    Repository.uploadRemoteFile(Repository.REMOTEDATABASECONFIGPATH, stream, f.getName());
                    
                    Files.copy(f.toPath(), new File(Repository.getConfigDirectory()+
                    Repository.getBar()+f.getName()).toPath(), REPLACE_EXISTING);
                    Repository.resetDBConf(f.getName(),false);}
                catch(Exception e){
                    saved = false;
                    e.printStackTrace();}
                if(saved){
                    CustomDialog.showInfo(JOptionPane.INFORMATION_MESSAGE, 
                                            DBConfig.this, "Successfull", 
                                            "File successfully uploaded");}
                else{
                    CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                            DBConfig.this, "Warning", 
                                            "File could not uploaded");}}});
        add(upload);
        JLabel database = new JLabel("Database: ");
        database.setBounds(15,55,90,20);
        add(database);
        tdatabase = new JTextField();
        tdatabase.setBounds(100,55,170,25);
        add(tdatabase);
        JLabel server = new JLabel("Server: ");
        server.setBounds(15,80,90,20);
        add(server);
        tserver = new JTextField();
        tserver.setBounds(100,80,170,25);
        add(tserver);
        JLabel user = new JLabel("User: ");
        user.setBounds(15,105,50,20);
        add(user);
        tuser = new JTextField();
        tuser.setBounds(100,105,170,25);
        add(tuser);
        JLabel password = new JLabel("Password: ");
        password.setBounds(15,130,90,20);
        add(password);
        tpassword = new JPasswordField();
        tpassword.setBounds(100,130,170,25);
        add(tpassword);
        refresh();
        JButton save = new JButton("Save");
        save.setBounds(200,155,70,20);
        save.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(doc!=null){
                    if(tpassword.getPassword().length == 0){
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                                DBConfig.this, "Warning", 
                                                "Warning, password not set");}
                    boolean saved = true;
                    try{theone = new File(Repository.temp+Repository.getBar()+"Twister"+
                        Repository.getBar()+"config"+Repository.getBar()+new File(
                        Repository.REMOTEDATABASECONFIGFILE).getName());
                        try{NodeList nodeLst = doc.getElementsByTagName("server");
                            if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.
                                item(0).getChildNodes().item(0).setNodeValue(tserver.getText());
                            else nodeLst.item(0).appendChild(doc.createTextNode(
                                tserver.getText()));
                            nodeLst = doc.getElementsByTagName("database");
                            if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.
                                item(0).getChildNodes().item(0).setNodeValue(tdatabase.
                                getText());
                            else nodeLst.item(0).appendChild(doc.createTextNode(tdatabase.
                                getText()));
                            nodeLst = doc.getElementsByTagName("user");
                            if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.
                                item(0).getChildNodes().item(0).setNodeValue(tuser.getText());
                            else nodeLst.item(0).appendChild(doc.createTextNode(tuser.
                                getText()));
                            if(tpassword.getPassword().length != 0 && !(new String(
                                tpassword.getPassword()).equals("****"))){
                                    nodeLst = doc.getElementsByTagName("password");
                                    if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.
                                        item(0).getChildNodes().item(0).setNodeValue(new String(
                                        tpassword.getPassword()));
                                    else nodeLst.item(0).appendChild(doc.createTextNode(
                                        new String(tpassword.getPassword())));}}
                        catch(Exception e){
                            saved = false;
                            System.out.println(doc.getDocumentURI()+
                            " may not be properly formatted");}
                        Result result = new StreamResult(theone);
                        try{DOMSource source = new DOMSource(doc);
                            TransformerFactory transformerFactory = TransformerFactory.
                            newInstance();
                            Transformer transformer = transformerFactory.newTransformer();
                            transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
                            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
                            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");                        
                            transformer.transform(source, result);  
                            
                            
//                             try{Repository.c.cd(Repository.REMOTEDATABASECONFIGPATH);}
//                             catch(Exception e){
//                                 System.out.println("could not get "+Repository.REMOTEDATABASECONFIGPATH);
//                                 e.printStackTrace();}
                            FileInputStream input = new FileInputStream(theone);
//                             Repository.c.put(input, theone.getName());
//                             input.close();
                            
                            
                            Repository.uploadRemoteFile(Repository.REMOTEDATABASECONFIGPATH, input, theone.getName());
                        
                        
                        }
                        catch(Exception e){
                            saved = false;
                            e.printStackTrace();
                            System.out.println("Could not save in file : "+Repository.
                            temp+Repository.getBar()+"Twister"+Repository.getBar()+"Config"+
                            Repository.getBar()+Repository.REMOTEDATABASECONFIGFILE+" and send to "+
                            Repository.REMOTEDATABASECONFIGPATH);}}
                    catch(Exception e){
                        saved = false;
                        e.printStackTrace();}
                    if(saved){
                        CustomDialog.showInfo(JOptionPane.INFORMATION_MESSAGE, 
                                                DBConfig.this, "Successfull", 
                                                "File successfully saved");}
                    else{
                        CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE, 
                                                DBConfig.this, "Warning", 
                                                "File could not be saved ");}}}});
        add(save);}
    
    public void refresh(){
        try{
            
            tserver.setText("");
            tdatabase.setText("");
            tpassword.setText("");
            tuser.setText("");
            
            
            
//             InputStream in = null;
//             try{Repository.c.cd(Repository.REMOTEDATABASECONFIGPATH);
//                 in = Repository.c.get(Repository.REMOTEDATABASECONFIGFILE);}
//             catch(Exception e){e.printStackTrace();
//                 System.out.println("Could not get: "+Repository.REMOTEDATABASECONFIGFILE);}
//             byte [] data = new byte[100];
//             ByteArrayOutputStream buffer = new ByteArrayOutputStream();
//             int nRead;
//             theone = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.
//                             getBar()+"config"+Repository.getBar()+
//                             new File(Repository.REMOTEDATABASECONFIGFILE).getName());
//             try{while ((nRead = in.read(data, 0, data.length)) != -1){buffer.write(data, 0, nRead);}
//                 buffer.flush();
//                 FileOutputStream out = new FileOutputStream(theone);
//                 buffer.writeTo(out);
//                 out.close();
//                 buffer.close();
//                 in.close();}
//             catch(Exception e){e.printStackTrace();
//                 //CustomDialog.showInfo(JOptionPane.INFORMATION_MESSAGE, null, "info", e.getMessage());
//                 System.out.println("Could not write "+Repository.REMOTEDATABASECONFIGFILE+" on local hdd");}
                
                
            theone = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.
                            getBar()+"config"+Repository.getBar()+
                            new File(Repository.REMOTEDATABASECONFIGFILE).getName());
            String content = Repository.getRemoteFileContent(Repository.REMOTEDATABASECONFIGPATH+Repository.REMOTEDATABASECONFIGFILE);
            BufferedWriter writer = new BufferedWriter(new FileWriter(theone));
            writer.write(content);
            writer.close();
            
                
            try{DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
                DocumentBuilder db = dbf.newDocumentBuilder();                                        
                doc = db.parse(theone);
                doc.getDocumentElement().normalize();
                NodeList nodeLst = doc.getElementsByTagName("server");
                tserver.setText(nodeLst.item(0).getChildNodes().item(0).getNodeValue());
                nodeLst = doc.getElementsByTagName("database");
                tdatabase.setText(nodeLst.item(0).getChildNodes().item(0).getNodeValue());
                nodeLst = doc.getElementsByTagName("password");
                tpassword.setText(nodeLst.item(0).getChildNodes().item(0).getNodeValue());
                if(!tpassword.getPassword().equals(""))tpassword.setText("****");
                nodeLst = doc.getElementsByTagName("user");
                tuser.setText(nodeLst.item(0).getChildNodes().item(0).getNodeValue());}
            catch(Exception e){
                System.out.println(Repository.temp+Repository.getBar()+
                "Twister"+Repository.getBar()+"Config"+Repository.getBar()+new File(Repository.
                REMOTEDATABASECONFIGFILE).getName()+" is corrupted or incomplete");
                e.printStackTrace();}}
        catch(Exception e){
            CustomDialog.showInfo(JOptionPane.INFORMATION_MESSAGE, null, "info", e.getMessage());
            e.printStackTrace();
            System.out.println("Could not refresh dbconfig structure");}}}
