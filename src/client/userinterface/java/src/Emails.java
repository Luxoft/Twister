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

public class Emails extends JPanel{
    public  JPanel p1;
    private JCheckBox check;
    private JTextField tipname, tport, tuser, tfrom;
    private JPasswordField tpass;
    private JTextArea emails, message, subject;
    private JLabel enable;

    public Emails(){
        setLayout(null);
        setPreferredSize(new Dimension(450,480));
        setBorder(BorderFactory.createBevelBorder(BevelBorder.LOWERED));
        setBackground(Color.WHITE);
        TitledBorder border = BorderFactory.createTitledBorder("SMTP server");
        border.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        JPanel p1 = new JPanel();
        p1.setBackground(Color.WHITE);
        p1.setBorder(border);         
        p1.setLayout(null);    
        p1.setBounds(80,5,350,68);
        JLabel ipname = new JLabel("IP/Name: ");
        ipname.setBounds(60,15,60,20);
        p1.add(ipname);
        tipname = new JTextField();
        tipname.setBounds(125,15,150,20);
        p1.add(tipname);
        JLabel port = new JLabel("Port: ");
        port.setBounds(60,40,60,20);
        p1.add(port);
        tport = new JTextField();
        tport.setBounds(125,40,150,20);
        p1.add(tport);
        add(p1);
        border = BorderFactory.createTitledBorder("Authentication");
        border.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        JPanel p2 = new JPanel();
        p2.setBackground(Color.WHITE);
        p2.setBorder(border);         
        p2.setLayout(null);    
        p2.setBounds(80,73,350,93);
        JLabel user = new JLabel("User: ");
        user.setBounds(60,15,60,20);
        p2.add(user);
        tuser = new JTextField();
        tuser.setBounds(125,15,150,20);
        p2.add(tuser);
        JLabel pass = new JLabel("Password: ");
        pass.setBounds(60,40,80,20);
        p2.add(pass);
        tpass = new JPasswordField();
        tpass.setBounds(125,40,150,20);
        p2.add(tpass);
        JLabel from = new JLabel("From: ");
        from.setBounds(60,65,60,20);
        p2.add(from);
        tfrom = new JTextField();
        tfrom.setBounds(125,65,150,20);
        p2.add(tfrom);
        add(p2);
        border = BorderFactory.createTitledBorder("Email List");
        border.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        JPanel p3 = new JPanel();
        p3.setBackground(Color.WHITE);
        p3.setBorder(border);         
        p3.setLayout(null);    
        p3.setBounds(80,170,350,68);
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
        p5.setBounds(80,240,350,58);
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
        p4.setBounds(80,300,350,108);
        message = new JTextArea();
        message.setLineWrap(true);
        message.setWrapStyleWord(true);
        JScrollPane scroll2 = new JScrollPane(message);
        scroll2.setBounds(7,18,336,85);
        p4.add(scroll2);        
        add(p4);
        enable = new JLabel("Disabled");
        enable.setBounds(360,410,60,20);
        add(enable);
        check = new JCheckBox();
        check.setBounds(412,410,20,20);
        check.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(check.isSelected())enable.setText("Enabled");
                else enable.setText("Disabled");}});
        add(check);
        JButton save = new JButton("Save");
        save.setBounds(352,435,80,20);
        save.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(tpass.getPassword().length == 0){JOptionPane.showMessageDialog(Emails.this, "Warning, password not set.", "Warning", JOptionPane.WARNING_MESSAGE);}
                try{
                    File theone = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+"Config"+Repository.getBar()+new File(Repository.REMOTEEMAILCONFIGFILE).getName());
                    DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
                    DocumentBuilder db = dbf.newDocumentBuilder();                                        
                    Document doc = db.parse(theone);
                    doc.getDocumentElement().normalize();
                    try{
                        NodeList nodeLst = doc.getElementsByTagName("Enabled");
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(check.isSelected()+"");
                        else nodeLst.item(0).appendChild(doc.createTextNode(check.isSelected()+""));
                        nodeLst = doc.getElementsByTagName("SMTPPath");
                        String SMTPPath = tipname.getText()+":"+tport.getText();
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(SMTPPath);
                        else nodeLst.item(0).appendChild(doc.createTextNode(SMTPPath));
                        nodeLst = doc.getElementsByTagName("SMTPUser");
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(tuser.getText());
                        else nodeLst.item(0).appendChild(doc.createTextNode(tuser.getText()));
                        if(tpass.getPassword().length != 0 && !(new String(tpass.getPassword()).equals("****"))){
                            nodeLst = doc.getElementsByTagName("SMTPPwd");
                            if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(new String(tpass.getPassword()));
                            else nodeLst.item(0).appendChild(doc.createTextNode(new String(tpass.getPassword())));}
                        nodeLst = doc.getElementsByTagName("From");
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(tfrom.getText());
                        else nodeLst.item(0).appendChild(doc.createTextNode(tfrom.getText()));
                        nodeLst = doc.getElementsByTagName("To");
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(emails.getText());
                        else nodeLst.item(0).appendChild(doc.createTextNode(emails.getText()));
                        nodeLst = doc.getElementsByTagName("Message");
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(message.getText());
                        else nodeLst.item(0).appendChild(doc.createTextNode(message.getText()));
                        nodeLst = doc.getElementsByTagName("Subject");
                        if(nodeLst.item(0).getChildNodes().getLength()>0)nodeLst.item(0).getChildNodes().item(0).setNodeValue(subject.getText());
                        else nodeLst.item(0).appendChild(doc.createTextNode(subject.getText()));}
                    catch(Exception e){System.out.println(doc.getDocumentURI()+" may not be properly formatted");}
                    Result result = new StreamResult(theone); 
                    try{DOMSource source = new DOMSource(doc);
                        TransformerFactory transformerFactory = TransformerFactory.newInstance();
                        Transformer transformer = transformerFactory.newTransformer();
                        transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
                        transformer.setOutputProperty(OutputKeys.INDENT, "yes");
                        transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");                        
                        transformer.transform(source, result);  
                        try{Repository.c.cd(Repository.REMOTEEMAILCONFIGPATH);}
                        catch(Exception e){System.out.println("could not get "+Repository.REMOTEEMAILCONFIGPATH);
                            e.printStackTrace();}
                        FileInputStream input = new FileInputStream(theone);
                        Repository.c.put(input, theone.getName());
                        input.close();}
                    catch(Exception e){e.printStackTrace();
                    System.out.println("Could not save in file : "+Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+"Config"+Repository.getBar()+Repository.REMOTEEMAILCONFIGFILE+" and send to "+Repository.REMOTEEMAILCONFIGPATH);}}
                catch(Exception e){e.printStackTrace();}}});
        add(save);}
    
    public void setIPName(String ipname){
        tipname.setText(ipname);}
        
    public void setPassword(String password){
        tpass.setText(password);}
    
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