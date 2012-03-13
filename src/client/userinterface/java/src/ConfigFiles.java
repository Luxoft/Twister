import javax.swing.JPanel;
//import net.sf.vfsjfilechooser.filepane.VFSFilePane;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
//import net.sf.vfsjfilechooser.utils.VFSUtils;
import net.sf.vfsjfilechooser.VFSJFileChooser;
//import net.sf.vfsjfilechooser.demo.Main;
import net.sf.vfsjfilechooser.accessories.DefaultAccessoriesPanel;
//import static net.sf.vfsjfilechooser.constants.VFSJFileChooserConstants.SELECTED_FILE_CHANGED_PROPERTY;
import org.apache.commons.vfs.FileObject;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.dom.DOMSource;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerConfigurationException;
import org.w3c.dom.Element;
import java.io.File;
import java.io.FileInputStream;
import javax.xml.transform.Result;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.Comment;
import javax.swing.JOptionPane;
import java.util.ArrayList;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import java.io.InputStream;
import java.io.FileOutputStream;
import java.io.ByteArrayOutputStream;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import java.awt.Component;
import java.awt.HeadlessException;
import javax.swing.JDialog;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.Container;
//import net.sf.vfsjfilechooser.plaf.metal.MetalVFSFileChooserUI;
import java.awt.Color;
import javax.swing.plaf.ComponentUI;
//import net.sf.vfsjfilechooser.filechooser.AbstractVFSFileSystemView;
//import net.sf.vfsjfilechooser.filechooser.AbstractVFSFileView;
import java.awt.GridLayout;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import java.awt.Font;
import javax.swing.border.TitledBorder;
import javax.swing.JTextArea;
import java.awt.Dimension;
import javax.swing.Box;
import javax.swing.BorderFactory;
import javax.swing.border.BevelBorder;
import java.awt.BorderLayout;

public class ConfigFiles extends JPanel{
    VFSJFileChooser fileChooser;
    private static JTextField ttcpath,tMasterXML,tUsers,tepid,tlog,trunning,tname,thardwareconfig,tdebug,tsummary,tinfo,tcli,tdbfile,tceport,traPort,thttpPort;
    JPanel paths;
    
    
    public ConfigFiles(Dimension screensize,DUT dut){  
        paths = new JPanel();
        paths.setBackground(Color.WHITE);
        paths.setLayout(null);
        paths.setPreferredSize(new Dimension(970,930));
        paths.setBorder(BorderFactory.createBevelBorder(BevelBorder.LOWERED));
        setLayout(null);        
        JPanel p1 = new JPanel();
        p1.setBackground(Color.WHITE);
        TitledBorder border = BorderFactory.createTitledBorder("TestCase Source Path");
        border.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        p1.setBorder(border);         
        p1.setLayout(new BoxLayout(p1, BoxLayout.Y_AXIS));    
        p1.setBounds(80,5,800,63);
        paths.add(p1);
        JTextArea tcpath = new JTextArea(" Master directory with the test cases that can be runned by the framework");
        tcpath.setWrapStyleWord(true);
        tcpath.setLineWrap(true);
        tcpath.setEditable(false);        
        tcpath.setCursor(null);  
        tcpath.setOpaque(false);  
        tcpath.setFocusable(false);         
        tcpath.setFont(new Font("Arial",Font.PLAIN,12));
        tcpath.setBackground(getBackground());
        tcpath.setMaximumSize(new Dimension(170,20));        
        tcpath.setPreferredSize(new Dimension(170,20));
        JPanel p11 = new JPanel();
        p11.setBackground(Color.WHITE);
        p11.setLayout(new GridLayout());
        p11.add(tcpath);
        p11.setMaximumSize(new Dimension(700,13));
        p11.setPreferredSize(new Dimension(700,13));
        ttcpath = new JTextField();
        ttcpath.setMaximumSize(new Dimension(340,20));
        ttcpath.setPreferredSize(new Dimension(340,20));
        ttcpath.setText(Repository.TESTSUITEPATH);
        JButton b = new JButton("...");  
        b.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(fileChooser==null)initializeFileBrowser();
                try{
                    if(fileChooser.showOpenDialog(Repository.f)==VFSJFileChooser.RETURN_TYPE.CANCEL){
                        FileObject aFileObject = fileChooser.getSelectedFile();
                        if(aFileObject!=null)ttcpath.setText(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).substring(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).indexOf("/")));}
                        fileChooser=null;}
                catch(Exception e){
                    fileChooser=null;
                    e.printStackTrace();}}});      
        b.setMaximumSize(new Dimension(50,20));
        b.setPreferredSize(new Dimension(50,20));
        JPanel p12 = new JPanel();
        p12.setBackground(Color.WHITE);
        p12.add(ttcpath);
        p12.add(b);
        p12.setMaximumSize(new Dimension(700,25));
        p12.setPreferredSize(new Dimension(700,25));
        p1.add(p11);
        p1.add(p12);        
        JPanel p2 = new JPanel();
        p2.setBackground(Color.WHITE);
        TitledBorder border2 = BorderFactory.createTitledBorder("Master XML TestSuite");
        border2.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border2.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        p2.setBorder(border2);    
        p2.setLayout(new BoxLayout(p2, BoxLayout.Y_AXIS));    
        p2.setBounds(80,68,800,63);
        paths.add(p2);     
        JTextArea masterXML = new JTextArea("Location of the XML that is generated from the user interface to run on Central Engine");        
        masterXML.setWrapStyleWord(true);        
        masterXML.setLineWrap(true);
        masterXML.setEditable(false);        
        masterXML.setCursor(null);  
        masterXML.setOpaque(false);   
        masterXML.setFocusable(false);      
        masterXML.setFont(new Font("Arial",Font.PLAIN,12));
        masterXML.setBackground(getBackground());        
        masterXML.setMaximumSize(new Dimension(170,20));        
        masterXML.setPreferredSize(new Dimension(170,20));   
        JPanel p21 = new JPanel();
        p21.setBackground(Color.WHITE);
        p21.setLayout(new GridLayout());
        p21.add(masterXML);        
        p21.setMaximumSize(new Dimension(700,13));
        p21.setPreferredSize(new Dimension(700,13));
        tMasterXML = new JTextField();
        tMasterXML.setMaximumSize(new Dimension(340,20));
        tMasterXML.setPreferredSize(new Dimension(340,20));        
        tMasterXML.setText(Repository.XMLREMOTEDIR);        
        JButton b2 = new JButton("...");        
        b2.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(fileChooser==null)initializeFileBrowser();
                try{if(fileChooser.showOpenDialog(Repository.f)==VFSJFileChooser.RETURN_TYPE.CANCEL){
                         FileObject aFileObject = fileChooser.getSelectedFile();
                         if(aFileObject!=null)tMasterXML.setText(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).substring(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).indexOf("/")));}
                         fileChooser=null;}
                 catch(Exception e){
                     fileChooser=null;
                     e.printStackTrace();}}});
        b2.setMaximumSize(new Dimension(50,20));
        b2.setPreferredSize(new Dimension(50,20));
        JPanel p22 = new JPanel();
        p22.setBackground(Color.WHITE);
        p22.add(tMasterXML);
        p22.add(b2);
        p22.setMaximumSize(new Dimension(700,25));
        p22.setPreferredSize(new Dimension(700,25));
        p2.add(p21);
        p2.add(p22);                     
        JPanel p3 = new JPanel();
        p3.setBackground(Color.WHITE);
        TitledBorder border3 = BorderFactory.createTitledBorder("Users Path");
        border3.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border3.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        p3.setBorder(border3);
        p3.setLayout(new BoxLayout(p3, BoxLayout.Y_AXIS));    
        p3.setBounds(80,131,800,63);
        paths.add(p3);        
        JTextArea Users = new JTextArea("Location of users XML files");
        Users.setWrapStyleWord(true);
        Users.setLineWrap(true);
        Users.setEditable(false);        
        Users.setCursor(null);  
        Users.setOpaque(false);  
        Users.setFocusable(false);         
        Users.setFont(new Font("Arial",Font.PLAIN,12));
        Users.setBackground(getBackground());
        Users.setMaximumSize(new Dimension(170,20));
        Users.setPreferredSize(new Dimension(170,20));   
        JPanel p31 = new JPanel();
        p31.setBackground(Color.WHITE);
        p31.setLayout(new GridLayout());
        p31.setMaximumSize(new Dimension(700,13));
        p31.setPreferredSize(new Dimension(700,13));
        p31.add(Users);        
        tUsers = new JTextField();
        tUsers.setMaximumSize(new Dimension(340,20));
        tUsers.setPreferredSize(new Dimension(340,20));   
        tUsers.setText(Repository.REMOTEUSERSDIRECTORY);        
        JButton b3 = new JButton("...");
        b3.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(fileChooser==null)initializeFileBrowser();
                try{if(fileChooser.showOpenDialog(Repository.f)==VFSJFileChooser.RETURN_TYPE.CANCEL){
                         FileObject aFileObject = fileChooser.getSelectedFile();
                         if(aFileObject!=null)tUsers.setText(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).substring(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).indexOf("/")));}
                         fileChooser=null;}
                 catch(Exception e){
                     fileChooser=null;
                     e.printStackTrace();}}});
        b3.setMaximumSize(new Dimension(50,20));
        b3.setPreferredSize(new Dimension(50,20));
        JPanel p32 = new JPanel();
        p32.setBackground(Color.WHITE);
        p32.add(tUsers);
        p32.add(b3);
        p32.setMaximumSize(new Dimension(700,25));
        p32.setPreferredSize(new Dimension(700,25));
        p3.add(p31);
        p3.add(p32);               
        JPanel p5 = new JPanel();
        p5.setBackground(Color.WHITE);
        TitledBorder border5 = BorderFactory.createTitledBorder("EPIds File");
        border5.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border5.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        p5.setBorder(border5);
        p5.setLayout(new BoxLayout(p5, BoxLayout.Y_AXIS));    
        p5.setBounds(80,194,800,63);
        paths.add(p5);              
        JTextArea epid = new JTextArea("Location of the file that contains the EpID list");
        epid.setWrapStyleWord(true);
        epid.setLineWrap(true);
        epid.setEditable(false);        
        epid.setCursor(null);  
        epid.setOpaque(false);  
        epid.setFocusable(false);         
        epid.setFont(new Font("Arial",Font.PLAIN,12));
        epid.setBackground(getBackground());
        epid.setMaximumSize(new Dimension(170,20));
        epid.setPreferredSize(new Dimension(170,20));   
        JPanel p51 = new JPanel();
        p51.setBackground(Color.WHITE);
        p51.setLayout(new GridLayout());
        p51.setMaximumSize(new Dimension(700,13));
        p51.setPreferredSize(new Dimension(700,13));
        p51.add(epid);
        tepid = new JTextField();
        tepid.setMaximumSize(new Dimension(340,20));
        tepid.setPreferredSize(new Dimension(340,20));
        tepid.setText(Repository.REMOTEEPIDDIR);
        JButton b5 = new JButton("...");
        b5.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(fileChooser==null)initializeFileBrowser();
                try{if(fileChooser.showOpenDialog(Repository.f)==VFSJFileChooser.RETURN_TYPE.CANCEL){
                         FileObject aFileObject = fileChooser.getSelectedFile();
                         if(aFileObject!=null)tepid.setText(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).substring(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).indexOf("/")));}
                         fileChooser=null;}
                 catch(Exception e){
                     fileChooser=null;
                     e.printStackTrace();}}});
        b5.setMaximumSize(new Dimension(50,20));
        b5.setPreferredSize(new Dimension(50,20));
        JPanel p52 = new JPanel();
        p52.setBackground(Color.WHITE);
        p52.setMaximumSize(new Dimension(700,25));
        p52.setPreferredSize(new Dimension(700,25));
        p52.add(tepid);
        p52.add(b5);
        p5.add(p51);
        p5.add(p52);
        JPanel p6 = new JPanel();
        p6.setBackground(Color.WHITE);
        TitledBorder border6 = BorderFactory.createTitledBorder("Logs Path");
        border6.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border6.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        p6.setBorder(border6);
        p6.setLayout(new BoxLayout(p6, BoxLayout.Y_AXIS));    
        p6.setBounds(80,257,800,63);
        paths.add(p6);
        JTextArea log = new JTextArea("Location of the directory that stores the logs that will be monitored");
        log.setWrapStyleWord(true);
        log.setLineWrap(true);
        log.setEditable(false);        
        log.setCursor(null);  
        log.setOpaque(false);  
        log.setFocusable(false);         
        log.setFont(new Font("Arial",Font.PLAIN,12));
        log.setBackground(getBackground());
        log.setMaximumSize(new Dimension(170,20));
        log.setPreferredSize(new Dimension(170,20));   
        JPanel p61 = new JPanel();
        p61.setBackground(Color.WHITE);
        p61.setLayout(new GridLayout());
        p61.setMaximumSize(new Dimension(700,13));
        p61.setPreferredSize(new Dimension(700,13));
        p61.add(log);        
        tlog = new JTextField();   
        tlog.setMaximumSize(new Dimension(340,20));
        tlog.setPreferredSize(new Dimension(340,20)); 
        tlog.setText(Repository.LOGSPATH);
        JButton b6 = new JButton("...");
        b6.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(fileChooser==null)initializeFileBrowser();
                try{if(fileChooser.showOpenDialog(Repository.f)==VFSJFileChooser.RETURN_TYPE.CANCEL){
                         FileObject aFileObject = fileChooser.getSelectedFile();
                         if(aFileObject!=null)tlog.setText(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).substring(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).indexOf("/")));}
                         fileChooser=null;}
                 catch(Exception e){
                     fileChooser=null;
                     e.printStackTrace();}}});
        b6.setMaximumSize(new Dimension(50,20));
        b6.setPreferredSize(new Dimension(50,20));
        JPanel p62 = new JPanel();
        p62.setBackground(Color.WHITE);
        p62.setMaximumSize(new Dimension(700,25));
        p62.setPreferredSize(new Dimension(700,25));
        p62.add(tlog);
        p62.add(b6);
        p6.add(p61);
        p6.add(p62);
        JPanel p7 = new JPanel();
        p7.setBackground(Color.WHITE);
        TitledBorder border7 = BorderFactory.createTitledBorder("Log Files");
        border7.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border7.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        p7.setBorder(border7);
        p7.setLayout(new BoxLayout(p7, BoxLayout.Y_AXIS));    
        p7.setBounds(80,320,800,165);
        paths.add(p7);              
        JTextArea log2 = new JTextArea("All the log files that will be monitored");
        log2.setWrapStyleWord(true);
        log2.setLineWrap(true);
        log2.setEditable(false);        
        log2.setCursor(null);  
        log2.setOpaque(false);  
        log2.setFocusable(false);         
        log2.setFont(new Font("Arial",Font.PLAIN,12));
        log2.setBackground(getBackground());
        log2.setMaximumSize(new Dimension(170,20));
        log2.setPreferredSize(new Dimension(170,20));   
        JPanel p71 = new JPanel();
        p71.setBackground(Color.WHITE);
        p71.setLayout(new GridLayout());
        p71.setMaximumSize(new Dimension(700,13));
        p71.setPreferredSize(new Dimension(700,13));
        p71.add(log2);
        JPanel p721 = new JPanel();
        p721.setBackground(Color.WHITE);
        trunning = new JTextField();
        trunning.setMaximumSize(new Dimension(340,20));
        trunning.setPreferredSize(new Dimension(340,20)); 
        if(Repository.logs.size()>0)trunning.setText(Repository.logs.get(0));
        JLabel l1 = new JLabel("Running: ");
        l1.setMaximumSize(new Dimension(65,20));
        l1.setPreferredSize(new Dimension(65,20));
        p721.add(l1);
        p721.add(trunning);
        p721.setMaximumSize(new Dimension(800,25));
        p721.setPreferredSize(new Dimension(800,25)); 
        tdebug = new JTextField();
        tdebug.setMaximumSize(new Dimension(340,20));
        tdebug.setPreferredSize(new Dimension(340,20)); 
        if(Repository.logs.size()>0)tdebug.setText(Repository.logs.get(1));
        JLabel l2 = new JLabel("Debug: ");
        l2.setMaximumSize(new Dimension(65,20));
        l2.setPreferredSize(new Dimension(65,20));
        JPanel p722 = new JPanel();
        p722.setBackground(Color.WHITE);
        p722.setMaximumSize(new Dimension(800,25));
        p722.setPreferredSize(new Dimension(800,25)); 
        p722.add(l2);
        p722.add(tdebug);        
        tsummary = new JTextField();
        tsummary.setMaximumSize(new Dimension(340,20));
        tsummary.setPreferredSize(new Dimension(340,20)); 
        if(Repository.logs.size()>0)tsummary.setText(Repository.logs.get(2));
        JLabel l3 = new JLabel("Summary: ");
        l3.setMaximumSize(new Dimension(65,20));
        l3.setPreferredSize(new Dimension(65,20));
        JPanel p723 = new JPanel();
        p723.setBackground(Color.WHITE);
        p723.setMaximumSize(new Dimension(800,25));
        p723.setPreferredSize(new Dimension(800,25)); 
        p723.add(l3);
        p723.add(tsummary); 
        tinfo = new JTextField();
        tinfo.setMaximumSize(new Dimension(340,20));
        tinfo.setPreferredSize(new Dimension(340,20)); 
        if(Repository.logs.size()>0)tinfo.setText(Repository.logs.get(3));
        JLabel l4 = new JLabel("Info: ");
        l4.setMaximumSize(new Dimension(65,20));
        l4.setPreferredSize(new Dimension(65,20));
        JPanel p724 = new JPanel();
        p724.setBackground(Color.WHITE);
        p724.setMaximumSize(new Dimension(800,25));
        p724.setPreferredSize(new Dimension(800,25)); 
        p724.add(l4);
        p724.add(tinfo); 
        tcli = new JTextField();
        tcli.setMaximumSize(new Dimension(340,20));
        tcli.setPreferredSize(new Dimension(340,20)); 
        if(Repository.logs.size()>0)tcli.setText(Repository.logs.get(4));
        JLabel l5 = new JLabel("Cli: ");
        l5.setMaximumSize(new Dimension(65,20));
        l5.setPreferredSize(new Dimension(65,20));
        JPanel p725 = new JPanel();
        p725.setBackground(Color.WHITE);
        p725.setMaximumSize(new Dimension(800,25));
        p725.setPreferredSize(new Dimension(800,25)); 
        p725.add(l5);
        p725.add(tcli); 
        JPanel p72 = new JPanel();
        p72.setBackground(Color.WHITE);
        p72.setLayout(new BoxLayout(p72, BoxLayout.Y_AXIS));
        p72.add(p721);
        p72.add(p722);
        p72.add(p723);
        p72.add(p724);
        p72.add(p725);
        p7.add(p71);
        p7.add(p72);
        JPanel p8 = new JPanel();
        p8.setBackground(Color.WHITE);
        TitledBorder border8 = BorderFactory.createTitledBorder("Hardware Config XML");
        border8.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border8.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        p8.setBorder(border8);
        p8.setLayout(new BoxLayout(p8, BoxLayout.Y_AXIS));    
        p8.setBounds(80,485,800,63);
        paths.add(p8);           
        JTextArea hardwareconfig = new JTextArea("Location of the XML file that contains the devices configuration");
        hardwareconfig.setWrapStyleWord(true);
        hardwareconfig.setLineWrap(true);
        hardwareconfig.setEditable(false);        
        hardwareconfig.setCursor(null);  
        hardwareconfig.setOpaque(false);  
        hardwareconfig.setFocusable(false);         
        hardwareconfig.setFont(new Font("Arial",Font.PLAIN,12));
        hardwareconfig.setBackground(getBackground());
        hardwareconfig.setMaximumSize(new Dimension(170,20));
        hardwareconfig.setPreferredSize(new Dimension(170,20));   
        JPanel p81 = new JPanel();
        p81.setBackground(Color.WHITE);
        p81.setLayout(new GridLayout());
        p81.setMaximumSize(new Dimension(700,13));
        p81.setPreferredSize(new Dimension(700,13));
        p81.add(hardwareconfig);
        thardwareconfig = new JTextField();
        thardwareconfig.setMaximumSize(new Dimension(340,20));
        thardwareconfig.setPreferredSize(new Dimension(340,20)); 
        thardwareconfig.setText(Repository.REMOTEHARDWARECONFIGDIRECTORY);
        JButton b7 = new JButton("...");
        b7.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(fileChooser==null)initializeFileBrowser();
                try{if(fileChooser.showOpenDialog(Repository.f)==VFSJFileChooser.RETURN_TYPE.CANCEL){
                        FileObject aFileObject = fileChooser.getSelectedFile();
                        if(aFileObject!=null)thardwareconfig.setText(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).substring(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).indexOf("/")));}
                        fileChooser=null;}
                catch(Exception e){
                    fileChooser=null;
                    e.printStackTrace();}}});
        b7.setMaximumSize(new Dimension(50,20));
        b7.setPreferredSize(new Dimension(50,20));
        JPanel p82 = new JPanel();
        p82.setBackground(Color.WHITE);
        p82.setMaximumSize(new Dimension(700,25));
        p82.setPreferredSize(new Dimension(700,25));
        p82.add(thardwareconfig);
        p82.add(b7);
        p8.add(p81);
        p8.add(p82);                     
        JPanel p9 = new JPanel();
        p9.setBackground(Color.WHITE);
        TitledBorder border9 = BorderFactory.createTitledBorder("File name");
        border9.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border9.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        p9.setBorder(border9);
        p9.setLayout(new BoxLayout(p9, BoxLayout.Y_AXIS));    
        p9.setBounds(80,801,800,63);
        paths.add(p9);          
        JTextArea name = new JTextArea("File name to store this configuration");
        name.setWrapStyleWord(true);
        name.setLineWrap(true);
        name.setEditable(false);        
        name.setCursor(null);  
        name.setOpaque(false);  
        name.setFocusable(false);         
        name.setFont(new Font("Arial",Font.PLAIN,12));
        name.setBackground(getBackground());
        name.setMaximumSize(new Dimension(170,20));
        name.setPreferredSize(new Dimension(170,20));   
        JPanel p91 = new JPanel();
        p91.setBackground(Color.WHITE);
        p91.setBackground(Color.WHITE);
        p91.setLayout(new GridLayout());
        p91.setMaximumSize(new Dimension(700,13));
        p91.setPreferredSize(new Dimension(700,13));
        p91.add(name);
        tname = new JTextField();
        tname.setMaximumSize(new Dimension(320,20));
        tname.setPreferredSize(new Dimension(320,20)); 
        JButton createXML = new JButton("Save");
        createXML.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(!tname.getText().equals("")){
                    saveXML(false);}
                else{JOptionPane.showMessageDialog(Repository.f, "No file name given", "Filename missing", JOptionPane.WARNING_MESSAGE);}}});
        createXML.setMaximumSize(new Dimension(70,20));
        createXML.setPreferredSize(new Dimension(70,20));
        JPanel p92 = new JPanel();
        p92.setBackground(Color.WHITE);
        p92.setMaximumSize(new Dimension(700,25));
        p92.setPreferredSize(new Dimension(700,25));
        p92.add(tname);
        p92.add(createXML);
        p9.add(p91);
        p9.add(p92);
        JPanel p10 = new JPanel();
        p10.setBackground(Color.WHITE);
        TitledBorder border10 = BorderFactory.createTitledBorder("Database XML path");
        border10.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border10.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        p10.setBorder(border10);
        p10.setLayout(new BoxLayout(p10, BoxLayout.Y_AXIS));    
        p10.setBounds(80,549,800,63);
        paths.add(p10);          
        JTextArea dbfile = new JTextArea("File location for database configuration");
        dbfile.setWrapStyleWord(true);
        dbfile.setLineWrap(true);
        dbfile.setEditable(false);        
        dbfile.setCursor(null);  
        dbfile.setOpaque(false);  
        dbfile.setFocusable(false);         
        dbfile.setFont(new Font("Arial",Font.PLAIN,12));
        dbfile.setBackground(getBackground());
        dbfile.setMaximumSize(new Dimension(170,20));
        dbfile.setPreferredSize(new Dimension(170,20));   
        JPanel p101 = new JPanel();
        p101.setBackground(Color.WHITE);
        p101.setBackground(Color.WHITE);
        p101.setLayout(new GridLayout());
        p101.setMaximumSize(new Dimension(700,13));
        p101.setPreferredSize(new Dimension(700,13));
        p101.add(dbfile);
        tdbfile = new JTextField();
        tdbfile.setMaximumSize(new Dimension(340,20));
        tdbfile.setPreferredSize(new Dimension(340,20)); 
        tdbfile.setText(Repository.REMOTEDATABASECONFIGPATH+Repository.REMOTEDATABASECONFIGFILE);
        JButton b8 = new JButton("...");
        b8.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(fileChooser==null)initializeFileBrowser();
                try{if(fileChooser.showOpenDialog(Repository.f)==VFSJFileChooser.RETURN_TYPE.CANCEL){
                        FileObject aFileObject = fileChooser.getSelectedFile();
                        if(aFileObject!=null)tdbfile.setText(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).substring(aFileObject.toString().substring(aFileObject.toString().indexOf("@")).indexOf("/")));}
                        fileChooser=null;}
                catch(Exception e){
                    fileChooser=null;
                    e.printStackTrace();}}});
        b8.setMaximumSize(new Dimension(50,20));
        b8.setPreferredSize(new Dimension(50,20));
        JPanel p102 = new JPanel();
        p102.setBackground(Color.WHITE);
        p102.setMaximumSize(new Dimension(700,25));
        p102.setPreferredSize(new Dimension(700,25));
        p102.add(tdbfile);
        p102.add(b8);
        p10.add(p101);
        p10.add(p102);
        JPanel p41 = new JPanel();
        p41.setBackground(Color.WHITE);
        TitledBorder border11 = BorderFactory.createTitledBorder("Central Engine Port");
        border11.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border11.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        p41.setBorder(border11);
        p41.setLayout(new BoxLayout(p41, BoxLayout.Y_AXIS));    
        p41.setBounds(80,612,800,63);
        paths.add(p41);          
        JTextArea ceport = new JTextArea("Central Engine port");
        ceport.setWrapStyleWord(true);
        ceport.setLineWrap(true);
        ceport.setEditable(false);        
        ceport.setCursor(null);  
        ceport.setOpaque(false);  
        ceport.setFocusable(false);         
        ceport.setFont(new Font("Arial",Font.PLAIN,12));
        ceport.setBackground(getBackground());
        ceport.setMaximumSize(new Dimension(170,20));
        ceport.setPreferredSize(new Dimension(170,20));   
        JPanel p411 = new JPanel();
        p411.setBackground(Color.WHITE);
        p411.setBackground(Color.WHITE);
        p411.setLayout(new GridLayout());
        p411.setMaximumSize(new Dimension(700,13));
        p411.setPreferredSize(new Dimension(700,13));
        p411.add(ceport);
        tceport = new JTextField();
        tceport.setMaximumSize(new Dimension(340,20));
        tceport.setPreferredSize(new Dimension(340,20)); 
        tceport.setText(Repository.getCentralEnginePort());
        JPanel p412 = new JPanel();
        p412.setBackground(Color.WHITE);
        p412.setMaximumSize(new Dimension(700,25));
        p412.setPreferredSize(new Dimension(700,25));
        p412.add(tceport);
        p41.add(p411);
        p41.add(p412);
        JPanel rapanel = new JPanel();
        rapanel.setBackground(Color.WHITE);
        TitledBorder border12 = BorderFactory.createTitledBorder("Resource Allocator Port");
        border12.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border12.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        rapanel.setBorder(border12);
        rapanel.setLayout(new BoxLayout(rapanel, BoxLayout.Y_AXIS));    
        rapanel.setBounds(80,675,800,63);
        paths.add(rapanel);          
        JTextArea raPort = new JTextArea("Resource Allocator Port");
        raPort.setWrapStyleWord(true);
        raPort.setLineWrap(true);
        raPort.setEditable(false);        
        raPort.setCursor(null);  
        raPort.setOpaque(false);  
        raPort.setFocusable(false);         
        raPort.setFont(new Font("Arial",Font.PLAIN,12));
        raPort.setBackground(getBackground());
        raPort.setMaximumSize(new Dimension(170,20));
        raPort.setPreferredSize(new Dimension(170,20));   
        JPanel rapanel1 = new JPanel();
        rapanel1.setBackground(Color.WHITE);
        rapanel1.setBackground(Color.WHITE);
        rapanel1.setLayout(new GridLayout());
        rapanel1.setMaximumSize(new Dimension(700,13));
        rapanel1.setPreferredSize(new Dimension(700,13));
        rapanel1.add(raPort);
        traPort = new JTextField();
        traPort.setMaximumSize(new Dimension(340,20));
        traPort.setPreferredSize(new Dimension(340,20)); 
        traPort.setText(Repository.getResourceAllocatorPort());
        JPanel rapanel2 = new JPanel();
        rapanel2.setBackground(Color.WHITE);
        rapanel2.setMaximumSize(new Dimension(700,25));
        rapanel2.setPreferredSize(new Dimension(700,25));
        rapanel2.add(traPort);
        rapanel.add(rapanel1);
        rapanel.add(rapanel2);
        JPanel httppanel = new JPanel();
        httppanel.setBackground(Color.WHITE);
        TitledBorder border13 = BorderFactory.createTitledBorder("HTTP Server Port");
        border13.setTitleFont(new Font("Arial",Font.PLAIN,14));
        border13.setBorder(BorderFactory.createLineBorder(new Color(150,150,150), 1));
        httppanel.setBorder(border13);
        httppanel.setLayout(new BoxLayout(httppanel, BoxLayout.Y_AXIS));    
        httppanel.setBounds(80,738,800,63);
        paths.add(httppanel);          
        JTextArea httpPort = new JTextArea("HTTP Server Port");
        httpPort.setWrapStyleWord(true);
        httpPort.setLineWrap(true);
        httpPort.setEditable(false);        
        httpPort.setCursor(null);  
        httpPort.setOpaque(false);  
        httpPort.setFocusable(false);         
        httpPort.setFont(new Font("Arial",Font.PLAIN,12));
        httpPort.setBackground(getBackground());
        httpPort.setMaximumSize(new Dimension(170,20));
        httpPort.setPreferredSize(new Dimension(170,20));   
        JPanel httppanel1 = new JPanel();
        httppanel1.setBackground(Color.WHITE);
        httppanel1.setBackground(Color.WHITE);
        httppanel1.setLayout(new GridLayout());
        httppanel1.setMaximumSize(new Dimension(700,13));
        httppanel1.setPreferredSize(new Dimension(700,13));
        httppanel1.add(httpPort);
        thttpPort = new JTextField();
        thttpPort.setMaximumSize(new Dimension(340,20));
        thttpPort.setPreferredSize(new Dimension(340,20)); 
        thttpPort.setText(Repository.getHTTPServerPort());
        JPanel httppanel2 = new JPanel();
        httppanel2.setBackground(Color.WHITE);
        httppanel2.setMaximumSize(new Dimension(700,25));
        httppanel2.setPreferredSize(new Dimension(700,25));
        httppanel2.add(thttpPort);
        httppanel.add(httppanel1);
        httppanel.add(httppanel2);
        
        
        
        
        
        
        
        JButton loadXML = new JButton("Load Config");
        loadXML.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){            
                try{
                    try{Repository.c.cd(Repository.USERHOME+"/twister/config/");}
                    catch(Exception e){System.out.println("Could not get: /home/tscguest/twister/Config/");}
                    int size = Repository.c.ls(Repository.USERHOME+"/twister/config/").size();
                    ArrayList<String> temp = new ArrayList<String>();
                    for(int i=0;i<size;i++){
                        String name = ((LsEntry)Repository.c.ls(Repository.USERHOME+"/twister/config/").get(i)).getFilename();
                        if(name.split("\\.").length==0)continue; 
                        if(name.indexOf(".xml")==-1)continue;                
                        temp.add(name);}
                    String configs [] = new String[temp.size()];
                    temp.toArray(configs);
                    String config = (String)JOptionPane.showInputDialog(null, "Please select a config", "config", 1, null, configs, "Configs");
                    if(config!=null){   
                        InputStream in = Repository.c.get(config);
                        byte [] data = new byte[100];
                        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
                        int nRead;
                        while ((nRead = in.read(data, 0, data.length)) != -1){buffer.write(data, 0, nRead);}
                        buffer.flush();
                        File theone = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+"config"+Repository.getBar()+config);
                        FileOutputStream out = new FileOutputStream(Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+"config"+Repository.getBar()+config);
                        buffer.writeTo(out);
                        out.close();
                        buffer.close();
                        in.close();                    
                        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
                        DocumentBuilder db = dbf.newDocumentBuilder();
                        Document doc=null;
                        try{doc = db.parse(theone);}
                        catch(Exception e){System.out.println(theone.getCanonicalPath()+" is corrup or not a valid XML");}
                        if(doc!=null){
                            doc.getDocumentElement().normalize();                
                            NodeList nodeLst = doc.getElementsByTagName("FileType");
                            if(nodeLst.getLength()>0){
                                Node fstNode = nodeLst.item(0);
                                Element fstElmnt = (Element)fstNode;
                                NodeList fstNm = fstElmnt.getChildNodes();
                                if(fstNm.item(0).getNodeValue().toString().equals("config")){
                                    in = new FileInputStream(theone);
                                    Repository.c.put(in, "fwmconfig.xml");
                                    in.close();
                                    Repository.emptyTestRepository();
                                    Repository.emptyLogs();
                                    File dir = new File(Repository.getUsersDirectory());
                                    String[] children = dir.list();
                                    for (int i=0; i<children.length; i++){new File(dir, children[i]).delete();}
                                    Repository.parseConfig();
                                    Repository.f.p.p2 = new Panel2(Repository.applet);
                                    Repository.f.p.setComponentAt(1, Repository.f.p.p2);
                                    Repository.f.p.p1.ep.refreshStructure();
                                    Repository.f.p.p4.dbconfig.refresh();
                                    Repository.resetDBConf(Repository.REMOTEDATABASECONFIGFILE,false);
                                    tdbfile.setText(Repository.REMOTEDATABASECONFIGFILE);
                                    ttcpath.setText(Repository.TESTSUITEPATH);
                                    tMasterXML.setText(Repository.XMLREMOTEDIR);
                                    tUsers.setText(Repository.REMOTEUSERSDIRECTORY);
                                    tepid.setText(Repository.REMOTEEPIDDIR);
                                    tlog.setText(Repository.LOGSPATH);
                                    thardwareconfig.setText(Repository.REMOTEHARDWARECONFIGDIRECTORY);
                                    if(Repository.logs.size()>0)trunning.setText(Repository.logs.get(0));
                                    trunning.setText(Repository.logs.get(0));
                                    tdebug.setText(Repository.logs.get(1));
                                    tsummary.setText(Repository.logs.get(2));
                                    tinfo.setText(Repository.logs.get(3));
                                    tcli.setText(Repository.logs.get(4));
                                    thardwareconfig.setText(Repository.REMOTEHARDWARECONFIGDIRECTORY);
                                    tdbfile.setText(Repository.REMOTEDATABASECONFIGPATH+Repository.REMOTEDATABASECONFIGFILE);
                                    thttpPort.setText(Repository.getHTTPServerPort());
                                    traPort.setText(Repository.getResourceAllocatorPort());
                                    tceport.setText(Repository.getCentralEnginePort());}
                                else JOptionPane.showMessageDialog(Repository.f, "This is not a config file", "WARNING", JOptionPane.WARNING_MESSAGE);}}
                        else JOptionPane.showMessageDialog(Repository.f, "Could not find Config tab", "WARNING", JOptionPane.WARNING_MESSAGE);}}
                catch(Exception e){e.printStackTrace();}}});
        loadXML.setBounds(760,870,120,20);
        paths.add(loadXML);}
        
        
    public static void saveXML(boolean blank){
        try{
            System.out.println("Starting saveXML");
            DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
            Document document = documentBuilder.newDocument();
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            DOMSource source = new DOMSource(document);                    
            Comment simpleComment = document.createComment("\n Master config file for TSC.\n \n Logs Path: Where CE and PE write their logs. Reports Path: Where all reports are saved.\n Test Suite Config: All info about the current Test Suite (Test Plan).\n");
            document.appendChild(simpleComment);
            Element root = document.createElement("Root");
            document.appendChild(root);
            Element rootElement = document.createElement("FileType");
            root.appendChild(rootElement);
            rootElement.appendChild(document.createTextNode("config"));
            rootElement = document.createElement("CentralEnginePort");
            root.appendChild(rootElement);
            String temp;
            if(blank) temp ="";
            else temp = tceport.getText();
            rootElement.appendChild(document.createTextNode(temp));
            rootElement = document.createElement("ResourceAllocatorPort");
            root.appendChild(rootElement);
            if(blank) temp ="";
            else temp = traPort.getText();
            rootElement.appendChild(document.createTextNode(temp));
            rootElement = document.createElement("HttpServerPort");
            root.appendChild(rootElement);
            if(blank) temp ="";
            else temp = thttpPort.getText();
            rootElement.appendChild(document.createTextNode(temp));
            rootElement = document.createElement("TestCaseSourcePath");
            root.appendChild(rootElement);
            if(blank) temp ="";
            else temp = ttcpath.getText();
            rootElement.appendChild(document.createTextNode(temp));
            rootElement = document.createElement("MasterXMLTestSuite");
            root.appendChild(rootElement);
            if(blank) temp ="";
            else temp = tMasterXML.getText();
            rootElement.appendChild(document.createTextNode(temp));
            rootElement = document.createElement("UsersPath");
            root.appendChild(rootElement);
            if(blank) temp ="";
            else temp = tUsers.getText();
            rootElement.appendChild(document.createTextNode(temp)); 
            rootElement = document.createElement("LogsPath");
            root.appendChild(rootElement);
            if(blank) temp ="";
            else temp = tlog.getText();
            rootElement.appendChild(document.createTextNode(temp));
            rootElement = document.createElement("LogFiles");
            root.appendChild(rootElement);
            Element subRootElement = document.createElement("logRunning");
            if(blank) temp ="";
            else temp = trunning.getText();
            subRootElement.appendChild(document.createTextNode(temp));
            rootElement.appendChild(subRootElement);
            subRootElement = document.createElement("logDebug");
            if(blank) temp ="";
            else temp = tdebug.getText();
            subRootElement.appendChild(document.createTextNode(temp));
            rootElement.appendChild(subRootElement);
            subRootElement = document.createElement("logSummary");
            if(blank) temp ="";
            else temp = tsummary.getText();
            subRootElement.appendChild(document.createTextNode(temp));
            rootElement.appendChild(subRootElement);
            subRootElement = document.createElement("logTest");
            if(blank) temp ="";
            else temp = tinfo.getText();
            subRootElement.appendChild(document.createTextNode(temp));
            rootElement.appendChild(subRootElement);
            subRootElement = document.createElement("logCli");
            if(blank) temp ="";
            else temp = tcli.getText();
            subRootElement.appendChild(document.createTextNode(temp));
            rootElement.appendChild(subRootElement);
            rootElement = document.createElement("DbConfigFile");
            root.appendChild(rootElement);
            if(blank) temp ="";
            else temp = tdbfile.getText();
            rootElement.appendChild(document.createTextNode(temp));
            rootElement = document.createElement("EPIdsFile");
            root.appendChild(rootElement);
            if(blank) temp ="";
            else temp = tepid.getText();
            rootElement.appendChild(document.createTextNode(temp));
            rootElement = document.createElement("HardwareConfig");
            root.appendChild(rootElement);
            if(blank) temp ="";
            else temp = thardwareconfig.getText();
            rootElement.appendChild(document.createTextNode(temp));
            if(blank) temp ="fwmconfig";
            else temp = tname.getText();
            File file = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+temp+".xml");
            Result result = new StreamResult(file);
            transformer.transform(source, result);
            Repository.c.cd(Repository.USERHOME+"/twister/config/");
            System.out.println("Saving to: "+Repository.USERHOME+"/twister/config/");
            FileInputStream in = new FileInputStream(file);
            Repository.c.put(in, file.getName());
            in.close();}
        catch(ParserConfigurationException e){System.out.println("DocumentBuilder cannot be created which satisfies the configuration requested");}
        catch(TransformerConfigurationException e){System.out.println("Could not create transformer");}
        catch(Exception e){e.printStackTrace();}}
        
    public void initializeFileBrowser(){
        fileChooser = new VFSJFileChooser("sftp://"+Repository.user+":"+Repository.password+"@"+Repository.host+"/home/"+Repository.user+"/twister/config/");        
        fileChooser.setFileHidingEnabled(true);
        fileChooser.setMultiSelectionEnabled(false);
        fileChooser.setFileSelectionMode(VFSJFileChooser.SELECTION_MODE.DIRECTORIES_ONLY);}}