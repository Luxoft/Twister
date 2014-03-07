/*
File: DatabaseInterface.java ; This file is part of Twister.
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
import javax.swing.JTextField;
import javax.swing.JLabel;
import javax.swing.JComboBox;
import javax.swing.JCheckBox;
import javax.swing.JButton;
import javax.swing.BoxLayout;
import javax.swing.BorderFactory;
import java.awt.FlowLayout;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import java.awt.Color;
import javax.swing.DefaultComboBoxModel;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.BorderLayout;
import javax.swing.JScrollPane;
import javax.swing.JPasswordField;
import java.awt.Component;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.File;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Text;
import org.w3c.dom.Node;
import org.w3c.dom.NamedNodeMap;
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
import java.io.FileInputStream;
import javax.swing.JFrame;
import javax.swing.JTabbedPane;
import javax.xml.bind.DatatypeConverter;

public class DatabaseInterface extends JPanel {
    
    private JButton fadd;
    private JComboBox fctype;
    private JPanel field;
    private JPanel fieldaddpanel;
    private JPanel fieldpanel;
    private JPanel insertpanel;
    private JButton iadd;
    private JLabel fromtable;
    private JPanel insertaddpanel;
    private JScrollPane jScrollPane0;
    private JScrollPane jScrollPane1;
    private JScrollPane jScrollPane2;
    private JScrollPane jScrollPane3;
    private JPanel maindatabasepanel;
    private JPanel mainfieldpanel;
    private JPanel maininsertpanel;
    private JPanel mainreportspanel;
    private JButton radd;
    private JPanel reportfieldpanel;
    private JPanel reportredirect;
    private JPanel reportreport;
    private JPanel reposrts;
    private JPanel reposrtsaddpanel;
    private JPanel database;
    private JComboBox sctype;
    private JPanel sql;
    private JLabel stype;
    private JTextField tid1,tlabel,tserver,tdatabase;
    private JPasswordField tpassword;
    private JTextField tuser;
    private String initialpass;
    private Node server,ndatabase,user,password;
    private Document doc;
    
    public DatabaseInterface() {
        initComponents();
        new Thread(){
            public void run(){
                while(!RunnerRepository.initialized){
                    try{Thread.sleep(100);}
                    catch(Exception e){e.printStackTrace();}
                }
                refresh();
            }
        }.start();
    }
    
    //parse db file and create 
    //gui fields 
    public void refresh(){
        mainfieldpanel.removeAll();
        mainfieldpanel.add(fieldaddpanel);
        maininsertpanel.removeAll();
        maininsertpanel.add(insertaddpanel);        
        mainreportspanel.removeAll();
        mainreportspanel.add(reposrtsaddpanel); 
        
        for(Component c:((JPanel)maindatabasepanel.getComponents()[0]).getComponents()){
            if(c.getClass()!=JLabel.class){
                ((JTextField)c).setText("");
            }
        }
        File theone=null;
        try{
            theone = new File(RunnerRepository.temp+RunnerRepository.getBar()+"Twister"+RunnerRepository.
                                    getBar()+"config"+RunnerRepository.getBar()+
                                    new File(RunnerRepository.REMOTEDATABASECONFIGFILE).getName());
            String content = new String(RunnerRepository.getRemoteFileContent(RunnerRepository.REMOTEDATABASECONFIGPATH+
                                                             RunnerRepository.REMOTEDATABASECONFIGFILE,false));
            BufferedWriter writer = new BufferedWriter(new FileWriter(theone));
            writer.write(content);
            writer.close();
        } catch (Exception e){
            System.out.println("There was an error in copying database config file from server to local pc");
            e.printStackTrace();
        }
        if(theone!=null){
            try{DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
                DocumentBuilder db = dbf.newDocumentBuilder();                                        
                doc = db.parse(theone);                
                doc.getDocumentElement().normalize();
                NodeList nodeLst = ((Element)doc.getFirstChild()).getElementsByTagName("db_config");
                if(nodeLst!=null&&nodeLst.getLength()==1){
                    Element el = (Element)nodeLst.item(0);
                    
                    NodeList content = el.getElementsByTagName("server");
                    if(content!=null&&content.getLength()==1){
                        try{server = content.item(0).getFirstChild();
                            tserver.setText(server.getNodeValue());}
                        catch(Exception e){
                            server = doc.createElement("");
                            content.item(0).appendChild(server);
                            tserver.setText("");}
                    } else {
                        System.out.println("server section is wrong configured in database file");
                    }
                    
                    content = el.getElementsByTagName("database");
                    if(content!=null&&content.getLength()==1){
                        try{ndatabase = content.item(0).getFirstChild();
                            tdatabase.setText(ndatabase.getNodeValue());}
                        catch(Exception e){
                            ndatabase = doc.createElement("");
                            content.item(0).appendChild(ndatabase);
                            tdatabase.setText("");}
                    } else {
                        System.out.println("database section is wrong configured in database file");
                    }
                    
                    content = el.getElementsByTagName("user");
                    if(content!=null&&content.getLength()==1){
                        try{user = content.item(0).getFirstChild();
                            tuser.setText(user.getNodeValue());}
                        catch(Exception e){
                            user = doc.createElement("");
                            content.item(0).appendChild(user);
                            tuser.setText("");}
                    } else {
                        System.out.println("user section is wrong configured in database file");
                    }
                    
                    content = el.getElementsByTagName("password");
                    if(content!=null&&content.getLength()==1){
                        try{password = content.item(0).getFirstChild();
                            tpassword.setText(password.getNodeValue());}
                        catch(Exception e){
                            password = doc.createElement("");
                            content.item(0).appendChild(password);
                            tpassword.setText("");}
                    } else {
                        System.out.println("password section is wrong configured in database file");
                    }
                    initialpass = new String(tpassword.getPassword());
                    
                } else {
                    System.out.println("db_config section is wrong configured in database file");
                }
                
                nodeLst = ((Element)doc.getFirstChild()).getElementsByTagName("insert_section");
                if(nodeLst!=null&&nodeLst.getLength()==1){
                    Element el = (Element)nodeLst.item(0);
                    
                    NodeList content = el.getElementsByTagName("field");
                    if(content!=null&&content.getLength()>0){
                        try{
                            Node n;
                            FieldPanel fpan;
                            mainfieldpanel.remove(fieldaddpanel);
                            NamedNodeMap props;
                            for(int i=0;i<content.getLength();i++){
                                n = content.item(i);
                                
                                fpan = new FieldPanel(mainfieldpanel);
                                mainfieldpanel.add(fpan);
                                props = n.getAttributes();
                                
                                setField(fpan.tid,props,"ID");
//                                 try{fpan.tid.setText(props.getNamedItem("ID").getNodeValue());}
//                                 catch(Exception e){}
                                setField(fpan.tfieldname,props,"FieldName");
//                                 try{fpan.tfieldname.setText(props.getNamedItem("FieldName").getNodeValue());}
//                                 catch(Exception e){}
                                setField(fpan.tfromtable,props,"FromTable");
//                                 try{fpan.tfromtable.setText(props.getNamedItem("FromTable").getNodeValue());}
//                                 catch(Exception e){}
                                setField(fpan.tlabel,props,"Label");
//                                 try{fpan.tlabel.setText(props.getNamedItem("Label").getNodeValue());}
//                                 catch(Exception e){}
                                setField(fpan.tquery,props,"SQLQuery");
//                                 try{fpan.tquery.setText(props.getNamedItem("SQLQuery").getNodeValue());}
//                                 catch(Exception e){}
                                try{fpan.mandatory.setSelected(Boolean.parseBoolean(props.getNamedItem("Mandatory").getNodeValue()));}
                                catch(Exception e){}
                                try{fpan.guidef.setSelected(Boolean.parseBoolean(props.getNamedItem("GUIDefined").getNodeValue()));}
                                catch(Exception e){}
                                try{String type = props.getNamedItem("Type").getNodeValue();
                                    for(int j=0;j<fpan.fctype.getItemCount();j++){
                                        String s = fpan.fctype.getItemAt(j).toString();
                                        if(s.equals(type)){
                                            fpan.fctype.setSelectedIndex(j);
                                            break;
                                        }
                                    }
                                } catch(Exception e){e.printStackTrace();}
                            }
                            mainfieldpanel.add(fieldaddpanel);
                            if(RunnerRepository.window!=null){
                                RunnerRepository.window.mainpanel.p4.revalidate();
                                RunnerRepository.window.mainpanel.p4.repaint();
                            }
                        }
                        catch(Exception e){
                            e.printStackTrace();
                        }
                    } else {
                        System.out.println("there are no fields in insert_section in database config file ");
                    }
                    
                    content = el.getElementsByTagName("sql_statement");
                    if(content!=null&&content.getLength()>0){
                        Node n;
                        maininsertpanel.remove(insertaddpanel);
                        for(int i=0;i<content.getLength();i++){
                            n = content.item(i);
                            InsertPanel inp =new InsertPanel(maininsertpanel);
                            maininsertpanel.add(inp);
                            try{inp.tsqlstatement.setText(n.getFirstChild().getNodeValue());}
                            catch(Exception e){}
                        }
                        maininsertpanel.add(insertaddpanel);
                        if(RunnerRepository.window!=null){
                            RunnerRepository.window.mainpanel.p4.revalidate();
                            RunnerRepository.window.mainpanel.p4.repaint();
                        }
                    } else {
                        System.out.println("there are no sql_statements in insert_section in database config file ");
                    }
                    
                } else {
                    System.out.println("insert_section section is wrong configured in database file");
                }
                
                nodeLst = ((Element)doc.getFirstChild()).getElementsByTagName("reports_section");
                if(nodeLst!=null&&nodeLst.getLength()==1){
                    Element el = (Element)nodeLst.item(0);
                    NodeList content = el.getElementsByTagName("field");
                    if(content!=null&&content.getLength()>0){
                        try{
                            Node n;
                            FieldPanel fpan;
                            NamedNodeMap props;
                            mainreportspanel.remove(reposrtsaddpanel);
                            for(int i=0;i<content.getLength();i++){
                                n = content.item(i);
                                ReportFieldPanel ipan = new ReportFieldPanel(mainreportspanel);
                                mainreportspanel.add(ipan);
                                props = n.getAttributes();
                                
                                setField(ipan.tid3,props,"ID");
//                                 try{ipan.tid3.setText(props.getNamedItem("ID").getNodeValue());}
//                                 catch(Exception e){}
                                setField(ipan.tlabel1,props,"Label");
//                                 try{ipan.tlabel1.setText(props.getNamedItem("Label").getNodeValue());}
//                                 catch(Exception e){}
                                setField(ipan.tquery1,props,"SQLQuery");
//                                 try{ipan.tquery1.setText(props.getNamedItem("SQLQuery").getNodeValue());}
//                                 catch(Exception e){}
                                
                                try{String type = props.getNamedItem("Type").getNodeValue();
                                    for(int j=0;j<ipan.fctype5.getItemCount();j++){
                                        String s = ipan.fctype5.getItemAt(j).toString();
                                        if(s.equals(type)){
                                            ipan.fctype5.setSelectedIndex(j);
                                            break;
                                        }
                                    }
                                } catch(Exception e){e.printStackTrace();}
                            }
                            mainreportspanel.add(reposrtsaddpanel);
                            if(RunnerRepository.window!=null){
                                RunnerRepository.window.mainpanel.p4.revalidate();
                                RunnerRepository.window.mainpanel.p4.repaint();
                            }
                        }
                        catch(Exception e){
                            e.printStackTrace();
                        }
                    } else {
                        System.out.println("there are no fields in reports_section in database config file ");
                    }
                    content = el.getElementsByTagName("report");
                    if(content!=null&&content.getLength()>0){
                        try{
                            Node n;
                            FieldPanel fpan;
                            NamedNodeMap props;
                            mainreportspanel.remove(reposrtsaddpanel);
                            for(int i=0;i<content.getLength();i++){
                                n = content.item(i);
                                ReportReport ipan = new ReportReport(mainreportspanel);
                                mainreportspanel.add(ipan);
                                props = n.getAttributes();
                                
                                setField(ipan.tid4,props,"ID");
//                                 try{ipan.tid4.setText(props.getNamedItem("ID").getNodeValue());}
//                                 catch(Exception e){}
                                setField(ipan.tquery4,props,"SQLTotal");
//                                 try{ipan.tquery4.setText(props.getNamedItem("SQLTotal").getNodeValue());}
//                                 catch(Exception e){}
                                setField(ipan.tquery3,props,"SQLQuery");
//                                 try{ipan.tquery3.setText(props.getNamedItem("SQLQuery").getNodeValue());}
//                                 catch(Exception e){}
                                
                                try{String type = props.getNamedItem("Type").getNodeValue();
                                    for(int j=0;j<ipan.fctype3.getItemCount();j++){
                                        String s = ipan.fctype3.getItemAt(j).toString();
                                        if(s.equals(type)){
                                            ipan.fctype3.setSelectedIndex(j);
                                            break;
                                        }
                                    }
                                } catch(Exception e){e.printStackTrace();}
                            }
                            mainreportspanel.add(reposrtsaddpanel);
                            if(RunnerRepository.window!=null){
                                RunnerRepository.window.mainpanel.p4.revalidate();
                                RunnerRepository.window.mainpanel.p4.repaint();
                            }
                        }
                        catch(Exception e){
                            e.printStackTrace();
                        }
                    } else {
                        System.out.println("there are no report s in reports_section in database config file ");
                    }
                    content = el.getElementsByTagName("redirect");
                    if(content!=null&&content.getLength()>0){
                        try{
                            Node n;
                            FieldPanel fpan;
                            NamedNodeMap props;
                            mainreportspanel.remove(reposrtsaddpanel);
                            for(int i=0;i<content.getLength();i++){
                                n = content.item(i);
                                ReportRedirect ipan = new ReportRedirect(mainreportspanel);
                                mainreportspanel.add(ipan);
                                props = n.getAttributes();
                                
                                setField(ipan.tquery5,props,"ID");
//                                 try{ipan.tquery5.setText(props.getNamedItem("ID").getNodeValue());}
//                                 catch(Exception e){}
                                setField(ipan.tquery6,props,"Path");
//                                 try{ipan.tquery6.setText(props.getNamedItem("Path").getNodeValue());}
//                                 catch(Exception e){}
                            }
                            mainreportspanel.add(reposrtsaddpanel);
                            if(RunnerRepository.window!=null){
                                RunnerRepository.window.mainpanel.p4.revalidate();
                                RunnerRepository.window.mainpanel.p4.repaint();
                            }
                        }
                        catch(Exception e){
                            e.printStackTrace();
                        }
                    } else {
                        System.out.println("there are no report s in reports_section in database config file ");
                    }
                } else {
                    System.out.println("reports_section section is wrong configured in database file");
                }
            }
            catch(Exception e){
                System.out.println(RunnerRepository.temp+RunnerRepository.getBar()+
                "Twister"+RunnerRepository.getBar()+"Config"+RunnerRepository.getBar()+new File(RunnerRepository.
                REMOTEDATABASECONFIGFILE).getName()+" is corrupted or incomplete");
                e.printStackTrace();
            }
        }
        if(RunnerRepository.window!=null){
            RunnerRepository.window.mainpanel.p4.revalidate();
            RunnerRepository.window.mainpanel.p4.repaint();
        }
        
    }
    
    //convenient method to set a field with given
    //NamedNodeMap prop
    private void setField(JTextField field, NamedNodeMap props, String prop){
        try{field.setText(props.getNamedItem(prop).getNodeValue());}
        catch(Exception e){}
    }
    
    //database gui section initialization
    private void initDatabasePanel(){
        JPanel d = new JPanel();
        d.setLayout(new GridBagLayout());
        GridBagConstraints gridBagConstraints = new GridBagConstraints();
        gridBagConstraints.gridx = 0;
        JLabel database = new JLabel("Database: "); 
        d.add(database,gridBagConstraints);
        gridBagConstraints.gridx = 1;
        tdatabase = new JTextField();  
        tdatabase.setPreferredSize(new Dimension(200,25));
        d.add(tdatabase,gridBagConstraints);
        gridBagConstraints.gridx = 0;
        JLabel server = new JLabel("Server: ");
        d.add(server,gridBagConstraints);
        gridBagConstraints.gridx = 1;
        tserver = new JTextField();   
        tserver.setPreferredSize(new Dimension(200,25));
        d.add(tserver,gridBagConstraints);
        gridBagConstraints.gridx = 0;
        JLabel user = new JLabel("User: ");  
        d.add(user,gridBagConstraints);
        gridBagConstraints.gridx = 1;
        tuser = new JTextField();  
        tuser.setPreferredSize(new Dimension(200,25));
        d.add(tuser,gridBagConstraints);
        gridBagConstraints.gridx = 0;
        JLabel password = new JLabel("Password: ");  
        d.add(password,gridBagConstraints);
        gridBagConstraints.gridx = 1;
        tpassword = new JPasswordField(); 
        tpassword.setPreferredSize(new Dimension(200,25));
        d.add(tpassword,gridBagConstraints);
        maindatabasepanel.add(d);
        if(!PermissionValidator.canEditDB()){
            tdatabase.setEnabled(false);
            tserver.setEnabled(false);
            tuser.setEnabled(false);
            tpassword.setEnabled(false);
        }
    }
    
    private void initComponents() {   
        setLayout(new BorderLayout());
        database = new JPanel();
        maindatabasepanel = new JPanel();
        maindatabasepanel.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK), "Database"));
        database.setLayout(new BorderLayout());        
        
        maindatabasepanel.setLayout(new BoxLayout(maindatabasepanel, BoxLayout.PAGE_AXIS));
        database.setMaximumSize(new Dimension(2000, 40));        
        initDatabasePanel();
        jScrollPane0 = new JScrollPane();
        jScrollPane0.setViewportView(maindatabasepanel);
        add(maindatabasepanel,BorderLayout.NORTH);
        field = new JPanel();
        jScrollPane1 = new JScrollPane();
        mainfieldpanel = new JPanel();        
        fieldaddpanel = new JPanel();
        fadd = new JButton();
        sql = new JPanel();
        jScrollPane2 = new JScrollPane();
        maininsertpanel = new JPanel();
        insertaddpanel = new JPanel();
        iadd = new JButton();
        reposrts = new JPanel();
        jScrollPane3 = new JScrollPane();
        mainreportspanel = new JPanel();        
        reposrtsaddpanel = new JPanel();
        stype = new JLabel();
        sctype = new JComboBox();
        radd = new JButton();
        field.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Field Section"));
        field.setLayout(new BorderLayout());
        mainfieldpanel.setLayout(new BoxLayout(mainfieldpanel, BoxLayout.PAGE_AXIS));
        fieldaddpanel.setMaximumSize(new Dimension(2000, 30));
        fieldaddpanel.setLayout(new FlowLayout(FlowLayout.CENTER, 0, 2));
        fadd.setText("  Add  ");
        fadd.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                mainfieldpanel.remove(fieldaddpanel);
                FieldPanel fpan = new FieldPanel(mainfieldpanel);
                mainfieldpanel.add(fpan);
                mainfieldpanel.add(fieldaddpanel);
                if(RunnerRepository.window!=null){
                    RunnerRepository.window.mainpanel.p4.revalidate();
                    RunnerRepository.window.mainpanel.p4.repaint();
                }
            }
        });
        fieldaddpanel.add(fadd);
        mainfieldpanel.add(fieldaddpanel);
        jScrollPane1.setViewportView(mainfieldpanel);
        field.add(jScrollPane1, BorderLayout.CENTER);
        sql.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Insert Section"));
        sql.setLayout(new BorderLayout());
        maininsertpanel.setLayout(new BoxLayout(maininsertpanel, BoxLayout.PAGE_AXIS));
        insertaddpanel.setMaximumSize(new Dimension(2000, 30));
        insertaddpanel.setLayout(new FlowLayout(FlowLayout.CENTER, 0, 2));
        iadd.setText("  Add  ");
        iadd.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                maininsertpanel.remove(insertaddpanel);
                InsertPanel ipan = new InsertPanel(maininsertpanel);
                maininsertpanel.add(ipan);
                maininsertpanel.add(insertaddpanel);
                if(RunnerRepository.window!=null){
                    RunnerRepository.window.mainpanel.p4.revalidate();
                    RunnerRepository.window.mainpanel.p4.repaint();
                }
            }
        });
        insertaddpanel.add(iadd);
        maininsertpanel.add(insertaddpanel);
        jScrollPane2.setViewportView(maininsertpanel);
        sql.add(jScrollPane2, BorderLayout.CENTER);
        reposrts.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(new Color(0, 0, 0)), "Reports Section"));
        reposrts.setLayout(new BorderLayout());
        mainreportspanel.setLayout(new BoxLayout(mainreportspanel, BoxLayout.PAGE_AXIS));
        reposrtsaddpanel.setMaximumSize(new Dimension(2000, 30));
        reposrtsaddpanel.setLayout(new FlowLayout(FlowLayout.CENTER, 4, 2));
        stype.setText("Type:");
        reposrtsaddpanel.add(stype);
        sctype.setModel(new DefaultComboBoxModel(new String[] { "field", "report", "redirect"}));
        reposrtsaddpanel.add(sctype);
        radd.setText("  Add  ");
        radd.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                mainreportspanel.remove(reposrtsaddpanel);
                JPanel ipan=null;
                switch(sctype.getSelectedIndex()){
                    case 0: 
                        ipan = new ReportFieldPanel(mainreportspanel);
                        break;                    
                    case 1:
                        ipan = new ReportReport(mainreportspanel);
                        break;
                    case 2:
                        ipan = new ReportRedirect(mainreportspanel);
                        break;
                }
                mainreportspanel.add(ipan);
                mainreportspanel.add(reposrtsaddpanel);
                if(RunnerRepository.window!=null){
                    RunnerRepository.window.mainpanel.p4.revalidate();
                    RunnerRepository.window.mainpanel.p4.repaint();
                }
            }
        });        
        reposrtsaddpanel.add(radd);
        mainreportspanel.add(reposrtsaddpanel);
        jScrollPane3.setViewportView(mainreportspanel);
        reposrts.add(jScrollPane3, BorderLayout.CENTER);
        
        JTabbedPane tab = new JTabbedPane();
        tab.add("Field Section", field);
        tab.add("Insert Section", sql);
        tab.add("Reports Section", reposrts);
        //add(tab,BorderLayout.CENTER);
        
        JPanel savepanel = new JPanel();
        savepanel.setLayout(new FlowLayout(FlowLayout.CENTER, 4, 2));
        JButton save = new JButton("Save File");
        save.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                generateFile();
            }});
        if(PermissionValidator.canEditDB()){
            savepanel.add(save);
        }
        add(savepanel,BorderLayout.SOUTH);
    }
    
    
    //generate db file
    private void generateFile(){
        try{
//             DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
//             DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
//             Document document = documentBuilder.newDocument();
//             TransformerFactory transformerFactory = TransformerFactory.newInstance();
//             Transformer transformer = transformerFactory.newTransformer();
//             transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
//             transformer.setOutputProperty(OutputKeys.INDENT, "yes");
//             transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
//             DOMSource source = new DOMSource(document);
//             Element root = document.createElement("root");
//             document.appendChild(root);
//             Element em = document.createElement("db_config");
//             Element subem = document.createElement("server");
//             subem.appendChild(document.createTextNode(tserver.getText()));
//             em.appendChild(subem);
            
            
            server.setNodeValue(tserver.getText());
            
            
//             subem = document.createElement("database");
//             subem.appendChild(document.createTextNode(tdatabase.getText()));
//             em.appendChild(subem);
            ndatabase.setNodeValue(tdatabase.getText());
            
//             subem = document.createElement("user");
//             subem.appendChild(document.createTextNode(tuser.getText()));
//             em.appendChild(subem);

            user.setNodeValue(tuser.getText());
//             subem = document.createElement("password");
            
            String p = new String(tpassword.getPassword());
            if(!initialpass.equals(p)){
                try{p = RunnerRepository.getRPCClient().execute("encryptText", new Object[]{p}).toString();
                    tpassword.setText(p);
                    initialpass = p;
                } catch(Exception e){
                    e.printStackTrace();
                }
            }
            
            password.setNodeValue(p);
            
//             subem.appendChild(document.createTextNode(p));
            
            
//             em.appendChild(subem);
//             root.appendChild(em);
//             em = document.createElement("insert_section");
//             root.appendChild(em);
            
//             for(Component c:mainfieldpanel.getComponents()){
//                 if(c.getClass()==FieldPanel.class){
//                     subem = document.createElement("field");
//                     subem.setAttribute("ID", ((FieldPanel)c).tid.getText());
//                     subem.setAttribute("FieldName", ((FieldPanel)c).tfieldname.getText());
//                     subem.setAttribute("FromTable", ((FieldPanel)c).tfromtable.getText());
//                     subem.setAttribute("Label", ((FieldPanel)c).tlabel.getText());
//                     subem.setAttribute("Mandatory", ((FieldPanel)c).mandatory.isSelected()+"");
//                     subem.setAttribute("SQLQuery", ((FieldPanel)c).tquery.getText());
//                     subem.setAttribute("Type", ((FieldPanel)c).fctype.getSelectedItem().toString());
//                     subem.setAttribute("GUIDefined", ((FieldPanel)c).guidef.isSelected()+"");
//                     em.appendChild(subem);
//                 }
//             }
            
//             for(Component c:maininsertpanel.getComponents()){
//                 if(c.getClass()==InsertPanel.class){
//                     subem = document.createElement("sql_statement");
//                     subem.appendChild(document.createTextNode(((InsertPanel)c).tsqlstatement.getText()));
//                     em.appendChild(subem);
//                 }
//             }
//             em = document.createElement("reports_section");
//             for(Component c:mainreportspanel.getComponents()){
//                 if(c.getClass()==ReportFieldPanel.class){
//                     subem = document.createElement("field");
//                     subem.setAttribute("ID", ((ReportFieldPanel)c).tid3.getText());
//                     subem.setAttribute("Label", ((ReportFieldPanel)c).tlabel1.getText());
//                     subem.setAttribute("SQLQuery", ((ReportFieldPanel)c).tquery1.getText());
//                     subem.setAttribute("Type", ((ReportFieldPanel)c).fctype5.getSelectedItem().toString());
//                     em.appendChild(subem);
//                 }else if(c.getClass()==ReportReport.class){
//                     subem = document.createElement("report");
//                     subem.setAttribute("ID", ((ReportReport)c).tid4.getText());
//                     subem.setAttribute("SQLQuery", ((ReportReport)c).tquery3.getText());
//                     subem.setAttribute("SQLTotal", ((ReportReport)c).tquery4.getText());
//                     subem.setAttribute("Type", ((ReportReport)c).fctype3.getSelectedItem().toString());
//                     em.appendChild(subem);
//                 }else if(c.getClass()==ReportRedirect.class){
//                     subem = document.createElement("redirect");
//                     subem.setAttribute("ID", ((ReportRedirect)c).tquery5.getText());
//                     subem.setAttribute("Path", ((ReportRedirect)c).tquery6.getText());
//                     em.appendChild(subem);
//                 }
//             }
//             root.appendChild(em);
            File file = new File(RunnerRepository.temp+RunnerRepository.getBar()+"Twister"+RunnerRepository.
                                  getBar()+"config"+RunnerRepository.getBar()+
                                  new File(RunnerRepository.REMOTEDATABASECONFIGFILE).getName());
            StreamResult result = new StreamResult(file);
            DOMSource source = new DOMSource(doc);
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            transformer.transform(source, result);
            FileInputStream in = new FileInputStream(file);
            RunnerRepository.uploadRemoteFile(RunnerRepository.REMOTEDATABASECONFIGPATH, in, file.getName(),false);
            CustomDialog.showInfo(JOptionPane.PLAIN_MESSAGE,RunnerRepository.window,
                                   "Success",
                                   "File successfully generated");
        } catch (Exception e){
            CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,RunnerRepository.window,
                                  "Warning",
                                  "WARNING! There was an error in generating the db file, please check log");
            e.printStackTrace();
        }
    }
}

class FieldPanel extends JPanel{
    public JTextField tid,tfieldname,tfromtable,tquery,tlabel;
    public JComboBox fctype;
    public JCheckBox guidef,mandatory;
    
    public FieldPanel(final JPanel parent){
        JLabel id = new JLabel();
        tid = new JTextField();        
        JLabel fieldname = new JLabel();
        tfieldname = new JTextField();        
        JLabel fromtable = new JLabel();
        tfromtable = new JTextField();        
        JLabel query = new JLabel();
        tquery = new JTextField();        
        JLabel label = new JLabel();
        tlabel = new JTextField();        
        JLabel ftype = new JLabel();
        fctype = new JComboBox();        
        guidef = new JCheckBox();        
        mandatory = new JCheckBox();        
        JButton jButton2 = new JButton();        
        setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
        setMaximumSize(new Dimension(2000, 25));
        setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
        id.setText("ID:");
        id.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(id);
        tid.setMaximumSize(new Dimension(500, 2147483647));
        tid.setPreferredSize(new Dimension(40, 20));
        tid.setMinimumSize(new Dimension(40, 20));
        add(tid);
        fieldname.setText("Field Name:");
        fieldname.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(fieldname);
        tfieldname.setMaximumSize(new Dimension(500, 2147483647));
        tfieldname.setPreferredSize(new Dimension(40, 20));
        add(tfieldname);
        fromtable.setText("From Table:");
        fromtable.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(fromtable);
        tfromtable.setMaximumSize(new Dimension(500, 2147483647));
        tfromtable.setPreferredSize(new Dimension(40, 20));
        add(tfromtable);
        query.setText("SQL Query");
        query.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(query);
        tquery.setMaximumSize(new Dimension(1500, 2147483647));
        tquery.setPreferredSize(new Dimension(120, 20));
        add(tquery);
        label.setText("Label:");
        label.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(label);
        tlabel.setMaximumSize(new Dimension(500, 2147483647));
        tlabel.setPreferredSize(new Dimension(40, 20));
        add(tlabel);
        ftype.setText("Type:");
        ftype.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(ftype);
        fctype.setModel(new DefaultComboBoxModel(new String[] { "DbSelect", "UserSelect", "UserText", "UserScript" }));
        fctype.setMaximumSize(new Dimension(250, 32767));
        add(fctype);
        guidef.setText("GUI Defined");
        add(guidef);
        mandatory.setText("Mandatory");
        add(mandatory);
        jButton2.setText("Remove");
        jButton2.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                parent.remove(FieldPanel.this);
                if(RunnerRepository.window!=null){
                    RunnerRepository.window.mainpanel.p4.revalidate();
                    RunnerRepository.window.mainpanel.p4.repaint();              
                }
            }
        });
        add(jButton2);
    }
}

class ReportFieldPanel extends JPanel{
    JComboBox fctype5;
    JTextField tid3;
    JTextField tlabel1;
    JTextField tquery1;
    
    public ReportFieldPanel(final JPanel parent){        
        JLabel id4 = new JLabel();
        tid3 = new JTextField();        
        JLabel query1 = new JLabel();
        tquery1 = new JTextField();        
        JLabel label1 = new JLabel();
        tlabel1 = new JTextField();        
        JLabel ftype1 = new JLabel();        
        fctype5 = new JComboBox();
        JButton remove = new JButton();
        setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
        setMaximumSize(new Dimension(2000, 25));
        setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
        id4.setText("ID:");
        id4.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(id4);
        tid3.setMaximumSize(new Dimension(500, 2147483647));
        tid3.setPreferredSize(new Dimension(40, 20));
        tid3.setMinimumSize(new Dimension(40, 20));
        add(tid3);
        query1.setText("SQL Query");
        query1.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(query1);
        tquery1.setMaximumSize(new Dimension(1500, 2147483647));
        tquery1.setPreferredSize(new Dimension(120, 20));
        add(tquery1);
        label1.setText("Label:");
        label1.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(label1);
        tlabel1.setMaximumSize(new Dimension(500, 2147483647));
        tlabel1.setPreferredSize(new Dimension(40, 20));
        add(tlabel1);
        ftype1.setText("Type:");
        ftype1.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(ftype1);
        fctype5.setModel(new DefaultComboBoxModel(new String[] { "UserSelect", "UserText"}));
        fctype5.setMaximumSize(new Dimension(250, 32767));
        add(fctype5);
        remove.setText("Remove");
        remove.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                parent.remove(ReportFieldPanel.this);
                if(RunnerRepository.window!=null){
                    RunnerRepository.window.mainpanel.p4.revalidate();
                    RunnerRepository.window.mainpanel.p4.repaint();  
                }
            }
        });
        add(remove);
    }
}

class ReportReport extends JPanel{
    JTextField tid4;
    JTextField tquery3;
    JTextField tquery4;
    JComboBox fctype3;
    
    public ReportReport(final JPanel parent){
        JLabel id6 = new JLabel();
        tid4 = new JTextField();
        JLabel query3 = new JLabel();
        tquery3 = new JTextField();
        JLabel sqltotal = new JLabel();
        tquery4 = new JTextField();
        JLabel ftype3 = new JLabel();
        fctype3 = new JComboBox();
        JButton jButton6 = new JButton();
        setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
        setMaximumSize(new Dimension(2000, 25));
        setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
        id6.setText("ID:");
        id6.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(id6);
        tid4.setMaximumSize(new Dimension(500, 2147483647));
        tid4.setMinimumSize(new Dimension(50, 20));
        tid4.setPreferredSize(new Dimension(50, 20));
        add(tid4);
        query3.setText("SQL Query");
        query3.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(query3);
        tquery3.setMaximumSize(new Dimension(1500, 2147483647));
        tquery3.setPreferredSize(new Dimension(150, 20));
        add(tquery3);
        sqltotal.setText("SQL Total:");
        sqltotal.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(sqltotal);
        tquery4.setMaximumSize(new Dimension(1500, 2147483647));
        tquery4.setPreferredSize(new Dimension(150, 20));
        add(tquery4);
        ftype3.setText("Type:");
        ftype3.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(ftype3);
        fctype3.setModel(new DefaultComboBoxModel(new String[] {"Table","BarChart","PieChart","LineChart"}));
        fctype3.setMaximumSize(new Dimension(250, 32767));
        add(fctype3);
        jButton6.setText("Remove");
        jButton6.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                parent.remove(ReportReport.this);
                if(RunnerRepository.window!=null){
                    RunnerRepository.window.mainpanel.p4.revalidate();
                    RunnerRepository.window.mainpanel.p4.repaint();  
                }
            }
        });
        add(jButton6);
    }
}

class ReportRedirect extends JPanel{
    JTextField tquery5;
    JTextField tquery6;
    
    public ReportRedirect(final JPanel parent){
        JLabel ID = new JLabel();
        tquery5 = new JTextField();
        JLabel query6 = new JLabel();
        tquery6 = new JTextField();
        JButton jButton7 = new JButton();
        setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
        setMaximumSize(new Dimension(2000, 25));
        setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
        ID.setText("ID:");
        ID.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(ID);
        tquery5.setMaximumSize(new Dimension(1500, 2147483647));
        tquery5.setPreferredSize(new Dimension(150, 20));
        add(tquery5);
        query6.setText("Path:");
        query6.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(query6);
        tquery6.setMaximumSize(new Dimension(1500, 2147483647));
        tquery6.setPreferredSize(new Dimension(150, 20));
        add(tquery6);
        jButton7.setText("Remove");
        jButton7.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                parent.remove(ReportRedirect.this);
                RunnerRepository.window.mainpanel.p4.revalidate();
                RunnerRepository.window.mainpanel.p4.repaint();  
            }
        });
        add(jButton7);
    }
}