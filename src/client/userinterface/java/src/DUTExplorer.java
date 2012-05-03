import javax.swing.JTree;
import javax.swing.tree.MutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreePath;
import javax.swing.tree.TreeModel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import java.awt.Color;
import java.awt.event.MouseEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import javax.swing.JTextField;
import javax.swing.JOptionPane;
import javax.swing.tree.TreeSelectionModel;
import javax.swing.plaf.metal.MetalIconFactory;
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.JButton;

public class DUTExplorer extends JPanel{
    JTree tree;
    DefaultMutableTreeNode root;
    
    public DUTExplorer(){
        setBounds(5,5,610,643);
        setLayout(null);
        setBackground(Color.RED);
        root = new DefaultMutableTreeNode("root", true);
        tree = new JTree(root);
        tree.setCellRenderer(new CustomIconRenderer());
        tree.expandRow(1);
        tree.setDragEnabled(false);
        tree.setRootVisible(false); 
        tree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
        ((DefaultTreeCellRenderer)(tree.getCellRenderer())).setLeafIcon(null);
        JScrollPane scroll = new JScrollPane(tree);
        scroll.setBounds(0,0,610,643);
        add(scroll);
        tree.addMouseListener(new MouseAdapter(){
            public void mouseReleased(MouseEvent ev){
                TreePath tp = tree.getPathForLocation(ev.getX(), ev.getY());
                if (tp != null){
                    if(ev.getButton() == MouseEvent.BUTTON3){                                          
                        tree.clearSelection();
                        if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Device){
                            tree.addSelectionPath(tp);
                            Repository.frame.mainpanel.p4.dut.nodetemp1 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            refreshPopup((DefaultMutableTreeNode)tp.getLastPathComponent(),ev,2);}
                        else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DeviceModule){
                            tree.addSelectionPath(tp);
                            Repository.frame.mainpanel.p4.dut.nodetemp2 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            refreshPopup((DefaultMutableTreeNode)tp.getLastPathComponent(),ev,1);}
                        else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DevicePort){
                            tree.addSelectionPath(tp);
                            Repository.frame.mainpanel.p4.dut.nodetemp3 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            refreshPopup((DefaultMutableTreeNode)tp.getLastPathComponent(),ev,0);}
                        else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof TestBed){
                            tree.addSelectionPath(tp);
                            Repository.frame.mainpanel.p4.dut.nodetemp0 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            refreshPopup((DefaultMutableTreeNode)tp.getLastPathComponent(),ev,3);}
                        else{Repository.frame.mainpanel.p4.dut.clearSelection();}}
                    else if(ev.getButton() == MouseEvent.BUTTON1){
                        if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Device){
                            Repository.frame.mainpanel.p4.dut.nodetemp1 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            if(Repository.frame.mainpanel.p4.dut.SettingsPanel.getComponentZOrder(Repository.frame.mainpanel.p4.dut.p2)==-1){
                                removeElements();
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.add(Repository.frame.mainpanel.p4.dut.p2);
                                Repository.frame.mainpanel.p4.dut.jScrollPane4.setViewportView(Repository.frame.mainpanel.p4.dut.properties);
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.revalidate();
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.repaint();}
                            ((Device)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject()).updateInfo();}
                        else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DeviceModule){
                            Repository.frame.mainpanel.p4.dut.nodetemp2 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            if(Repository.frame.mainpanel.p4.dut.SettingsPanel.getComponentZOrder(Repository.frame.mainpanel.p4.dut.p3)==-1){
                                removeElements();
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.add(Repository.frame.mainpanel.p4.dut.p3);
                                Repository.frame.mainpanel.p4.dut.jScrollPane4.setViewportView(Repository.frame.mainpanel.p4.dut.properties2);
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.revalidate();
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.repaint();}    
                            ((DeviceModule)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject()).updateInfo();}
                        else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof TestBed){
                            Repository.frame.mainpanel.p4.dut.nodetemp0 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            if(Repository.frame.mainpanel.p4.dut.SettingsPanel.getComponentZOrder(Repository.frame.mainpanel.p4.dut.p1)==-1){
                                removeElements();
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.add(Repository.frame.mainpanel.p4.dut.p1);
                                Repository.frame.mainpanel.p4.dut.jScrollPane4.setViewportView(null);
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.revalidate();
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.repaint();}    
                            ((TestBed)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject()).updateInfo();}
                        else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DevicePort){{
                            Repository.frame.mainpanel.p4.dut.nodetemp3 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            if(Repository.frame.mainpanel.p4.dut.SettingsPanel.getComponentZOrder(Repository.frame.mainpanel.p4.dut.p4)==-1){
                                removeElements();
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.add(Repository.frame.mainpanel.p4.dut.p4);
                                Repository.frame.mainpanel.p4.dut.jScrollPane4.setViewportView(Repository.frame.mainpanel.p4.dut.properties3);
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.revalidate();
                                Repository.frame.mainpanel.p4.dut.SettingsPanel.repaint();}
                            ((DevicePort)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject()).updateInfo();}}
                        else{Repository.frame.mainpanel.p4.dut.clearSelection();}}}
                else{Repository.frame.mainpanel.p4.dut.clearSelection(); 
                    tree.clearSelection();
                    if(ev.getButton() == MouseEvent.BUTTON3){ 
                        refreshPopup(null,ev,0);}}}});}
                        
    public void removeElements(){
        Repository.frame.mainpanel.p4.dut.SettingsPanel.remove(Repository.frame.mainpanel.p4.dut.p1);
        Repository.frame.mainpanel.p4.dut.SettingsPanel.remove(Repository.frame.mainpanel.p4.dut.p3);
        Repository.frame.mainpanel.p4.dut.SettingsPanel.remove(Repository.frame.mainpanel.p4.dut.p4);
        Repository.frame.mainpanel.p4.dut.jScrollPane4.remove(Repository.frame.mainpanel.p4.dut.properties2);
        Repository.frame.mainpanel.p4.dut.jScrollPane4.remove(Repository.frame.mainpanel.p4.dut.properties3);
        Repository.frame.mainpanel.p4.dut.SettingsPanel.remove(Repository.frame.mainpanel.p4.dut.p2);
        Repository.frame.mainpanel.p4.dut.jScrollPane4.remove(Repository.frame.mainpanel.p4.dut.properties);}
                
    public void refreshPopup(final DefaultMutableTreeNode element,MouseEvent ev,int type){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item;
        if(element == null){
            item = new JMenuItem("Add TestBed");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    addTestBed();}});
            p.add(item);}
        else if(type == 3){
            item = new JMenuItem("Add Device");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    addDevice(element);}});
            p.add(item);
            item = new JMenuItem("Remove TestBed");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    removeElement(element);}});
            p.add(item);}
        else if(type == 2){
            item = new JMenuItem("Add Module");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    addModule(element);}});
            p.add(item);
            item = new JMenuItem("Remove Device");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    removeElement(element);}});
            p.add(item);}
        else if(type == 1){
            item = new JMenuItem("Add Port");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    addPort(element);}});
            p.add(item);
            item = new JMenuItem("Remove module");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    removeElement(element);}});
            p.add(item);}
        else{item = new JMenuItem("Remove port");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    removeElement(element);}});
            p.add(item);}
        p.show(this.tree,ev.getX(),ev.getY());}
        
    public void removeElement(DefaultMutableTreeNode element){
        ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(element);
        Repository.frame.mainpanel.p4.dut.clearSelection();}
        
    public void addTestBed(){    
        JTextField name = new JTextField("");
        Object configs = new Object[]{"Name: ",name};
        int r = JOptionPane.showConfirmDialog(null, configs, "Add testbed", JOptionPane.OK_CANCEL_OPTION);  
        if (r == JOptionPane.OK_OPTION){
            TestBed d = new TestBed();
            d.setName(name.getText());
            DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
            DefaultMutableTreeNode child2 = new DefaultMutableTreeNode("Id: "+d.id,false);
            child.add(child2);
            DefaultMutableTreeNode child3 = new DefaultMutableTreeNode("Description: "+d.description,false);
            child.add(child3);
            ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, root,root.getChildCount());
            ((DefaultTreeModel)tree.getModel()).reload();}}
    
    public void addDevice(DefaultMutableTreeNode element){    
        JTextField name = new JTextField("");
        Object configs = new Object[]{"Name: ",name};
        int r = JOptionPane.showConfirmDialog(null, configs, "Add device", JOptionPane.OK_CANCEL_OPTION);  
        if (r == JOptionPane.OK_OPTION){
            Device d = new Device();
            d.setName(name.getText());
            DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
            DefaultMutableTreeNode child3 = new DefaultMutableTreeNode("Id: "+d.id,false);
            child.add(child3);
            DefaultMutableTreeNode child2 = new DefaultMutableTreeNode("Description: "+d.description,false);
            child.add(child2);
            DefaultMutableTreeNode child4 = new DefaultMutableTreeNode("Vendor: "+d.vendor,false);
            child.add(child4);
            DefaultMutableTreeNode child5 = new DefaultMutableTreeNode("Type: "+d.type,false);
            child.add(child5);
            DefaultMutableTreeNode child6 = new DefaultMutableTreeNode("Family: "+d.family,false);
            child.add(child6);
            DefaultMutableTreeNode child7 = new DefaultMutableTreeNode("Model: "+d.model,false);
            child.add(child7);
            ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, element,element.getChildCount());}}
            
    public void addModule(DefaultMutableTreeNode element){
        JTextField name = new JTextField("");
        Object configs = new Object[]{"Type: ",name};
        int r = JOptionPane.showConfirmDialog(null, configs, "Add module", JOptionPane.OK_CANCEL_OPTION);  
        if (r == JOptionPane.OK_OPTION){
            DeviceModule d = new DeviceModule(name.getText());
            DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
            DefaultMutableTreeNode child3 = new DefaultMutableTreeNode("Module Type: "+d.name);
            child.add(child3);
            ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, element,element.getChildCount());}}
            
    public void addPort(DefaultMutableTreeNode element){
        JTextField name = new JTextField("");
        JTextField type = new JTextField("");
        Object configs = new Object[]{"Port: ",name,"Port type: ",type};
        int r = JOptionPane.showConfirmDialog(null, configs, "Add port", JOptionPane.OK_CANCEL_OPTION);  
        if (r == JOptionPane.OK_OPTION){
            DevicePort d = new DevicePort(name.getText(),type.getText());
            DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
            DefaultMutableTreeNode child3 = new DefaultMutableTreeNode("Port type: "+type.getText());
            child.add(child3);
            ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, element,element.getChildCount());}}}