/*
File: DatabaseInterface.java ; This file is part of Twister.
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
import javax.swing.JTextField;
import javax.swing.JLabel;
import javax.swing.JComboBox;
import javax.swing.JCheckBox;
import javax.swing.JButton;
import javax.swing.BoxLayout;
import javax.swing.BorderFactory;
import java.awt.FlowLayout;
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
    private JTextField tid1;
    private JTextField tlabel;
    private JTextField tserver;
    private JTextField tdatabase;
    private JPasswordField tpassword;
    private JTextField tuser;
    
    public DatabaseInterface() {
        initComponents();
    }
    
    private void refresh(){
        mainfieldpanel.removeAll();
        mainfieldpanel.add(fieldaddpanel);
        maininsertpanel.removeAll();
        maininsertpanel.add(insertaddpanel);        
        mainreportspanel.removeAll();
        mainreportspanel.add(reposrtsaddpanel);        
        for(Component c:maindatabasepanel.getComponents()){
            if(c.getClass()!=JLabel.class){
                ((JTextField)c).setText("");
            }
        }
        File theone=null;
        try{
            theone = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.
                                    getBar()+"config"+Repository.getBar()+
                                    new File(Repository.REMOTEDATABASECONFIGFILE).getName());
            String content = Repository.getRemoteFileContent(Repository.REMOTEDATABASECONFIGPATH+
                                                             Repository.REMOTEDATABASECONFIGFILE);
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
                Document doc = db.parse(theone);                
                doc.getDocumentElement().normalize();
                NodeList nodeLst = ((Element)doc.getFirstChild()).getElementsByTagName("db_config");
                if(nodeLst!=null&&nodeLst.getLength()==1){
                    nodeLst = ((Element)nodeLst.item(0)).getElementsByTagName("server");
                    if(nodeLst!=null&&nodeLst.getLength()==1){
                        try{tserver.setText(nodeLst.item(0).getFirstChild().getNodeValue());}
                        catch(Exception e){tserver.setText("");}
                    } else {
                        System.out.println("server section is wrong configured in database file");
                    }
                    
                    
                    
                } else {
                    System.out.println("db_config section is wrong configured in database file");
                }
                
                
//                 NodeList nodeLst = doc.getElementsByTagName("server");
//                 try{tserver.setText(nodeLst.item(0).getChildNodes().item(0).getNodeValue());}
//                 catch(Exception e){
//                     tserver.setText("");
//                     e.printStackTrace();}
//                 nodeLst = doc.getElementsByTagName("database");
//                 tdatabase.setText(nodeLst.item(0).getChildNodes().item(0).getNodeValue());
//                 nodeLst = doc.getElementsByTagName("password");
//                 tpassword.setText(nodeLst.item(0).getChildNodes().item(0).getNodeValue());
//                 if(!tpassword.getPassword().equals(""))tpassword.setText("****");
//                 nodeLst = doc.getElementsByTagName("user");
//                 tuser.setText(nodeLst.item(0).getChildNodes().item(0).getNodeValue());
            }
            catch(Exception e){
                System.out.println(Repository.temp+Repository.getBar()+
                "Twister"+Repository.getBar()+"Config"+Repository.getBar()+new File(Repository.
                REMOTEDATABASECONFIGFILE).getName()+" is corrupted or incomplete");
                e.printStackTrace();
            }
        }
        revalidate();
        repaint();
    }
    
    private void initDatabasePanel(){
        JLabel database = new JLabel("Database: ");
        maindatabasepanel.add(database);        
        tdatabase = new JTextField();        
        maindatabasepanel.add(tdatabase);        
        JLabel server = new JLabel("Server: ");        
        maindatabasepanel.add(server);        
        tserver = new JTextField();        
        maindatabasepanel.add(tserver);        
        JLabel user = new JLabel("User: ");        
        maindatabasepanel.add(user);
        tuser = new JTextField();        
        maindatabasepanel.add(tuser);        
        JLabel password = new JLabel("Password: ");        
        maindatabasepanel.add(password);        
        tpassword = new JPasswordField();        
        maindatabasepanel.add(tpassword);
    }
    
    private void initComponents() {        
        database = new JPanel();
        database.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK), "Database"));
        database.setLayout(new BorderLayout());        
        maindatabasepanel = new JPanel();
        maindatabasepanel.setLayout(new BoxLayout(maindatabasepanel, BoxLayout.LINE_AXIS));
        database.setMaximumSize(new Dimension(2000, 40));        
        initDatabasePanel();
        jScrollPane0 = new JScrollPane();
        jScrollPane0.setViewportView(maindatabasepanel);
        database.add(jScrollPane0, BorderLayout.CENTER);        
        add(database);        
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
        setLayout(new BoxLayout(this, BoxLayout.PAGE_AXIS));
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
                revalidate();
                repaint();
            }
        });
        fieldaddpanel.add(fadd);
        mainfieldpanel.add(fieldaddpanel);
        jScrollPane1.setViewportView(mainfieldpanel);
        field.add(jScrollPane1, BorderLayout.CENTER);
        add(field);
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
                revalidate();
                repaint();
            }
        });
        insertaddpanel.add(iadd);
        maininsertpanel.add(insertaddpanel);
        jScrollPane2.setViewportView(maininsertpanel);
        sql.add(jScrollPane2, BorderLayout.CENTER);
        add(sql);
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
                revalidate();
                repaint();
            }
        });        
        reposrtsaddpanel.add(radd);
        mainreportspanel.add(reposrtsaddpanel);
        jScrollPane3.setViewportView(mainreportspanel);
        reposrts.add(jScrollPane3, BorderLayout.CENTER);
        add(reposrts);
        JPanel savepanel = new JPanel();
        savepanel.setLayout(new FlowLayout(FlowLayout.CENTER, 4, 2));
        JButton save = new JButton("Save File");
        save.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
            refresh();
            }});
        savepanel.add(save);
        add(savepanel);
    }
}

class FieldPanel extends JPanel{
    
    public FieldPanel(final JPanel parent){
        JLabel id = new JLabel();
        JTextField tid = new JTextField();        
        JLabel fieldname = new JLabel();
        JTextField tfieldname = new JTextField();        
        JLabel fromtable = new JLabel();
        JTextField tfromtable = new JTextField();        
        JLabel query = new JLabel();
        JTextField tquery = new JTextField();        
        JLabel label = new JLabel();
        JTextField tlabel = new JTextField();        
        JLabel ftype = new JLabel();
        JComboBox fctype = new JComboBox();        
        JCheckBox guidef = new JCheckBox();        
        JCheckBox mandatory = new JCheckBox();        
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
                parent.revalidate();
                parent.repaint();
            }
        });
        add(jButton2);
    }
}

class InsertPanel extends JPanel{
    
    public InsertPanel(final JPanel parent){
        JLabel id2 = new JLabel();
        JTextField tsqlstatement = new JTextField();        
        setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
        setMaximumSize(new Dimension(2000, 25));
        setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
        id2.setText("SQL Statement:");
        id2.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(id2);
        tsqlstatement.setMinimumSize(new Dimension(50, 20));
        add(tsqlstatement);        
        JButton jButton3 = new JButton();
        jButton3.setText("Remove");
        jButton3.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                parent.remove(InsertPanel.this);
                parent.revalidate();
                parent.repaint();
            }
        });
        add(jButton3);
    }
}

class ReportFieldPanel extends JPanel{
    public ReportFieldPanel(final JPanel parent){        
        JLabel id4 = new JLabel();
        JTextField tid3 = new JTextField();        
        JLabel query1 = new JLabel();
        JTextField tquery1 = new JTextField();        
        JLabel label1 = new JLabel();
        JTextField tlabel1 = new JTextField();        
        JLabel ftype1 = new JLabel();        
        JComboBox fctype5 = new JComboBox();
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
                parent.revalidate();
                parent.repaint();
            }
        });
        add(remove);
    }
}

class ReportReport extends JPanel{
    public ReportReport(final JPanel parent){
        JLabel id6 = new JLabel();
        JTextField tid4 = new JTextField();
        JLabel query3 = new JLabel();
        JTextField tquery3 = new JTextField();
        JLabel sqltotal = new JLabel();
        JTextField tquery4 = new JTextField();
        JLabel ftype3 = new JLabel();
        JComboBox fctype3 = new JComboBox();
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
                parent.revalidate();
                parent.repaint();
            }
        });
        add(jButton6);
    }
}

class ReportRedirect extends JPanel{
    public ReportRedirect(final JPanel parent){
        JLabel ID = new JLabel();
        JTextField tquery5 = new JTextField();
        JLabel query6 = new JLabel();
        JTextField tquery6 = new JTextField();
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
                parent.revalidate();
                parent.repaint();
            }
        });
        add(jButton7);
    }
}