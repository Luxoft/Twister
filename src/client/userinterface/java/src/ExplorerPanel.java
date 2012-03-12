import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import javax.swing.JScrollPane;
import javax.swing.JTree;
import javax.swing.tree.MutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.DefaultMutableTreeNode;
import java.io.File;
import java.awt.BorderLayout;
import java.awt.dnd.DragSource;
import java.awt.event.MouseAdapter;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseListener;
import java.awt.event.MouseEvent;
import javax.swing.TransferHandler;
import java.awt.dnd.DragSource;
import java.awt.dnd.DropTarget;
import java.awt.dnd.DnDConstants;
import java.awt.dnd.DragGestureListener;
import java.awt.dnd.DragGestureEvent;
import java.awt.dnd.DragSourceListener;
import javax.swing.tree.TreePath;
import java.awt.dnd.DragSourceDropEvent;
import java.awt.dnd.DragSourceDragEvent;
import java.awt.dnd.DragSourceEvent;
import java.awt.dnd.DragSourceContext;
import java.io.IOException;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import java.util.Vector;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import javax.xml.parsers.ParserConfigurationException;
import org.xml.sax.SAXException;
import java.io.IOException;
import java.util.Comparator;
import java.util.Collections;
import com.jcraft.jsch.SftpException;
import java.net.URL;
import java.net.URLConnection;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Scanner;
import java.awt.Container;
import javax.swing.tree.TreeModel;
import java.awt.Dimension;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import javax.swing.JTextArea;
import javax.swing.JFrame;
import javax.swing.JButton;
import java.awt.BorderLayout;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import java.awt.event.MouseMotionAdapter;
import javax.swing.text.PlainDocument;


public class ExplorerPanel extends JPanel {
    private static final long serialVersionUID = 1L;
    JTree tree;
    private DefaultMutableTreeNode root;
    private boolean dragging;
    private TreePath [] selected;
    private DefaultMutableTreeNode child2;
  
    public ExplorerPanel(int x, int y, TreeDropTargetListener tdtl, boolean applet, ChannelSftp c){
//         System.out.println("Started Explorer initialization: "+System.currentTimeMillis());
        Repository.intro.text = "Started Explorer interface initialization";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();
        setLayout(null);
        setSize(450,600);
        setPreferredSize(new Dimension(450,500));
        setMinimumSize(new Dimension(0,0));
        setMaximumSize(new Dimension(1000,1000));
        root = new DefaultMutableTreeNode("root", true);        
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance(); 
        try{Repository.c.cd(Repository.getTestSuitePath());}
        catch(Exception e){e.printStackTrace();}
//         System.out.println("Started getList(): "+System.currentTimeMillis());
        Repository.intro.text = "Started retrieving tc directories";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();
        getList(root,Repository.c);
//         System.out.println("Finished getList(): "+System.currentTimeMillis());
        Repository.intro.text = "Finished retrieving tc directories";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();
        tree = new JTree(root);
        tree.expandRow(1);
        tree.addMouseListener(new MouseAdapter(){
                public void mousePressed(MouseEvent ev){
                    if(ev.isPopupTrigger()){refreshPopup(ev);}
                    else{setDragging(true);
                        selected = tree.getSelectionPaths();
                        if(selected!=null){
                            int left  = 0;          
                            int right = selected.length-1;                        
                            while (left < right) {
                                TreePath temp = selected[left]; 
                                selected[left]  = selected[right]; 
                                selected[right] = temp;
                                left++;
                                right--;}}}}
                public void mouseReleased(MouseEvent ev){
                    if(ev.isPopupTrigger()){refreshPopup(ev);}
                    else{
                        if((tree.getSelectionPaths().length==1)&&(tree.getModel().isLeaf(tree.getSelectionPath().getLastPathComponent()))){
                            try{String thefile = tree.getSelectionPath().getParentPath().getLastPathComponent().toString()+"/"+tree.getSelectionPath().getLastPathComponent().toString();
                                XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
                                try{config.setServerURL(new URL("http://"+Repository.host+":"+Repository.getCentralEnginePort()));}
                                catch(Exception e){System.out.println("Could not connect to "+Repository.host+" on port "+Repository.getCentralEnginePort());}//!!! NU uita sa updatezi portul in mesajul de eroare                          
                                XmlRpcClient client = new XmlRpcClient();
                                client.setConfig(config);
                                String result= client.execute("getTestDescription",new Object[]{thefile})+"";
//                                 String endpoint = "http://"+Repository.host+"/pythontest/index2.py";
//                                 URL url = new URL(endpoint+"?"+"file="+thefile);
//                                 URLConnection conn = url.openConnection ();
//                                 Scanner scanner = new Scanner(new InputStreamReader(conn.getInputStream()));
//                                 StringBuffer buf = new StringBuffer();
//                                 while (scanner.hasNextLine()){buf.append(scanner.nextLine());}
//                                 scanner.close();
                                System.out.println("result: "+result);
                                String [] cont = result.split("-;-");
                                Container pan1 = (Container)Repository.f.p.p1.splitPane.getComponent(1);
                                TCDetails pan2 = (TCDetails)pan1.getComponents()[1];
                                if(cont[1].length()>1)pan2.text.setText(cont[1].substring(1));
                                else pan2.text.setText("Not Available");
                                if(cont[0].length()>1)pan2.title.setText(cont[0].substring(1));
                                else pan2.title.setText("Not Available");}
                            catch(Exception e){e.printStackTrace();}}}}});
        DragSource ds = new DragSource();
        ds.getDefaultDragSource();
        ds.createDefaultDragGestureRecognizer(this,DnDConstants.ACTION_COPY_OR_MOVE,new TreeDragGestureListener());
        tree.setDragEnabled(true);
        tree.setRootVisible(false);
//         System.out.println("Finished Explorer initialization: "+System.currentTimeMillis());
        Repository.intro.text = "Finished Explorer interface initialization";
        Repository.intro.percent+=0.035;
        Repository.intro.repaint();}
        
    public TreePath[] getSelected(){        
        Arrays.sort(selected, new Compare());
        List<TreePath> listOfPaths = Arrays.asList(selected);
        Collections.reverse(listOfPaths);
        selected = listOfPaths.toArray(new TreePath[]{});
        return selected;}
        
    public void refreshPopup(MouseEvent ev){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item = new JMenuItem("Refresh tree");        
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                refreshStructure();}});
        final String editable =  tree.getSelectionPath().getLastPathComponent()+"";
        if((tree.getSelectionPaths().length==1)&&(tree.getModel().isLeaf(tree.getSelectionPath().getLastPathComponent()))&&
        ((editable.indexOf(".tcl")!=-1)||(editable.indexOf(".py")!=-1)||(editable.indexOf(".pl")!=-1))){
            item = new JMenuItem("Edit");     
            p.add(item);
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    //System.out.println(tree.getSelectionPath().getPathComponent(tree.getSelectionPath().getPathCount()-2)+"/"+tree.getSelectionPath().getLastPathComponent());                    
                    final JFrame f = new JFrame();
                    //f.setLayout(new BorderLayout());
                    //Repository.f.setEnabled(false);
                    tree.setEnabled(false);
                    Repository.f.p.p1.sc.g.setCanRequestFocus(false);
                    //Repository.f.p.p1.sc.g.setEnabled(false);
                    f.setVisible(true);
                    f.setBounds(200,100,500,600);
                    final JEditTextArea textarea = new JEditTextArea();
                    textarea.getDocument().putProperty(PlainDocument.tabSizeAttribute, 4);
                    if(editable.indexOf(".tcl")!=-1)textarea.setTokenMarker(new TCLTokenMarker());
                    else if(editable.indexOf(".py")!=-1)textarea.setTokenMarker(new PythonTokenMarker());
                    else if(editable.indexOf(".pl")!=-1)textarea.setTokenMarker(new PerlTokenMarker());
                    
//                     f.add(textarea,BorderLayout.CENTER);
                    f.add(textarea);
                    JButton save = new JButton("Save");
                    save.setPreferredSize(new Dimension(70,20));
                    save.setMaximumSize(new Dimension(70,20));
//                     f.add(save,BorderLayout.PAGE_END);
                    final String filename = tree.getSelectionPath().getPathComponent(tree.getSelectionPath().getPathCount()-2)+"/"+tree.getSelectionPath().getLastPathComponent();                    
                    final File file = new File(Repository.temp+Repository.getBar()+"Twister"+Repository.getBar()+tree.getSelectionPath().getLastPathComponent());
                    JMenuBar menu = new JMenuBar();
                    //menu.setLayout(null);
                    //menu.setBounds(0, 0, width, 20);
                    JMenu filemenu = new JMenu("File");
                    //filemenu.setBounds(10,0,40,20);
                    JMenuItem saveuser = new JMenuItem("Save");
                    saveuser.addActionListener(new ActionListener() {
                        public void actionPerformed(ActionEvent ev){
                            try{BufferedWriter out = new BufferedWriter(new FileWriter(file));
                                out.write(textarea.getText());
                                out.close();
                                FileInputStream in = new FileInputStream(file);
                                Repository.c.put(in, filename);}
                            catch(Exception e){
                                e.printStackTrace();
                                System.out.println("There was a problem in saving file "+file.getName()+" on hdd ad uploading it to "+filename);}}});
                    filemenu.add(saveuser);
                    menu.add(filemenu);
                    f.setJMenuBar(menu);
//                     save.addActionListener(
//                         new ActionListener(){
//                             public void actionPerformed(ActionEvent ev){
//                                 try{BufferedWriter out = new BufferedWriter(new FileWriter(file));
//                                     out.write(textarea.getText());
//                                     out.close();
//                                     FileInputStream in = new FileInputStream(file);
//                                     Repository.c.put(in, filename);}
//                                 catch(Exception e){
//                                     e.printStackTrace();
//                                     System.out.println("There was a problem in saving file "+file.getName()+" on hdd ad uploading it to "+filename);}}});
                    InputStream in = null;
                    System.out.print("Getting "+filename+" ....");
                    try{in = Repository.c.get(filename);}
                    catch(Exception e){System.out.println("Could not get :"+filename);}
                    InputStreamReader inputStreamReader = new InputStreamReader(in);
                    BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
                    String line;
                    try{while ((line=bufferedReader.readLine())!= null){
                            textarea.appendText(line+"\n");}
                        bufferedReader.close();
                        inputStreamReader.close();
                        in.close();
                        textarea.setCaretPosition(0);
                        System.out.println("successfull");}
                    catch(Exception e){
                        System.out.println("failed");
                        e.printStackTrace();}
                    f.addWindowListener(new WindowAdapter(){
                        public void windowClosing(WindowEvent ev){
                            tree.setEnabled(true);
                            //Repository.f.p.p1.sc.g.setEnabled(true);
                            Repository.f.p.p1.sc.g.setCanRequestFocus(true);
                            //Repository.f.setEnabled(true);
                            file.delete();
                            textarea.setText("");
                            f.dispose();}});}});}
        p.show(tree,ev.getX(),ev.getY());}
        
    public void refreshStructure(){
        root.remove(0);
        try{Repository.c.cd(Repository.getTestSuitePath());
            getList(root,Repository.c);}           
        catch(Exception e){e.printStackTrace();}
        ((DefaultTreeModel)tree.getModel()).reload();
        tree.expandRow(0);
        selected = null;
        setDragging(false);}
        
    public void setDragging(boolean drag){
        dragging = drag;}
        
    public boolean getDragging(){
        return dragging;}

    public void getList(DefaultMutableTreeNode node, ChannelSftp c){
        try{DefaultMutableTreeNode child = new DefaultMutableTreeNode(c.pwd());
            Vector<LsEntry> vector1 = c.ls(".");
            Vector <String> vector = new Vector<String>();
            int lssize = vector1.size(); 
            if(lssize>2)node.add(child);
            for(int i=0;i<lssize;i++){
                vector.add(vector1.get(i).getFilename());}
            Collections.sort(vector);
            for(int i = 0; i<lssize; i++){
                if(vector.get(i).split("\\.").length==0)continue;
                try{c.cd(vector.get(i));
                    getList(child, c);
                    c.cd("..");}
                catch(SftpException e){
                    if(e.id==4){
                        child2 = new DefaultMutableTreeNode(vector.get(i));
                        child.add(child2);}
                    else e.printStackTrace();}}}
        catch(Exception e){e.printStackTrace();}}}

class Compare implements Comparator{   
    public int compare(Object emp1, Object emp2){ 
        return ((TreePath)emp1).getLastPathComponent().toString().compareToIgnoreCase(((TreePath)emp2).getLastPathComponent().toString());}}

class TreeDragGestureListener implements DragGestureListener {
    public void dragGestureRecognized(DragGestureEvent dragGestureEvent) {}}
          
class MyDragSourceListener implements DragSourceListener {
    public void dragDropEnd(DragSourceDropEvent dragSourceDropEvent) {}
    public void dragEnter(DragSourceDragEvent dragSourceDragEvent) {}
    public void dragExit(DragSourceEvent dragSourceEvent) {}
    public void dragOver(DragSourceDragEvent dragSourceDragEvent) {}
    public void dropActionChanged(DragSourceDragEvent dragSourceDragEvent) {}}