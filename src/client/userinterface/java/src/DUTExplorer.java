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
                        tree.addSelectionPath(tp);
                        if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Device){
                            Repository.f.p.p4.dut.nodetemp1 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            refreshPopup((DefaultMutableTreeNode)tp.getLastPathComponent(),ev,2);}
                        else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DeviceModule){
                            Repository.f.p.p4.dut.nodetemp2 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            refreshPopup((DefaultMutableTreeNode)tp.getLastPathComponent(),ev,1);}
                        else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DevicePort){
                            Repository.f.p.p4.dut.nodetemp3 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            refreshPopup((DefaultMutableTreeNode)tp.getLastPathComponent(),ev,0);}}
                    else if(ev.getButton() == MouseEvent.BUTTON1){
                        if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof Device){
                            Repository.f.p.p4.dut.nodetemp1 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            if(Repository.f.p.p4.dut.config.getComponentZOrder(Repository.f.p.p4.dut.p2)==-1){
                                Repository.f.p.p4.dut.config.remove(Repository.f.p.p4.dut.p3);
                                Repository.f.p.p4.dut.config.remove(Repository.f.p.p4.dut.p4);
                                Repository.f.p.p4.dut.config.add(Repository.f.p.p4.dut.p2);
                                Repository.f.p.p4.dut.config.repaint();}
                            ((Device)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject()).updateInfo();}
                        else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DeviceModule){
                            Repository.f.p.p4.dut.nodetemp2 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            if(Repository.f.p.p4.dut.config.getComponentZOrder(Repository.f.p.p4.dut.p3)==-1){
                                Repository.f.p.p4.dut.config.remove(Repository.f.p.p4.dut.p2);
                                Repository.f.p.p4.dut.config.remove(Repository.f.p.p4.dut.p4);
                                Repository.f.p.p4.dut.config.add(Repository.f.p.p4.dut.p3);
                                Repository.f.p.p4.dut.config.repaint();}    
                            ((DeviceModule)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject()).updateInfo();}
                        else if(((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject() instanceof DevicePort){{
                            Repository.f.p.p4.dut.nodetemp3 = (DefaultMutableTreeNode)tp.getLastPathComponent();
                            if(Repository.f.p.p4.dut.config.getComponentZOrder(Repository.f.p.p4.dut.p4)==-1){
                                Repository.f.p.p4.dut.config.remove(Repository.f.p.p4.dut.p3);
                                Repository.f.p.p4.dut.config.remove(Repository.f.p.p4.dut.p2);
                                Repository.f.p.p4.dut.config.add(Repository.f.p.p4.dut.p4);
                                Repository.f.p.p4.dut.config.repaint();}
                            ((DevicePort)((DefaultMutableTreeNode)tp.getLastPathComponent()).getUserObject()).updateInfo();}}}}
                else{
                    if(ev.getButton() == MouseEvent.BUTTON3){ 
                    refreshPopup(null,ev,0);}}}});}
                
    public void refreshPopup(final DefaultMutableTreeNode element,MouseEvent ev,int type){
        JPopupMenu p = new JPopupMenu();
        JMenuItem item;
        if(element == null){
            item = new JMenuItem("Add device");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    JTextField name = new JTextField("");
                    Object configs = new Object[]{"Name: ",name};
                    int r = JOptionPane.showConfirmDialog(null, configs, "Add device", JOptionPane.OK_CANCEL_OPTION);  
                    if (r == JOptionPane.OK_OPTION){
                        Device d = new Device();
                        d.setName(name.getText());
                        DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
//                         root.add(child);
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
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, root,root.getChildCount());
                        ((DefaultTreeModel)tree.getModel()).reload();}}});
            p.add(item);}
        else if(type == 2){
            item = new JMenuItem("Add Module");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    JTextField name = new JTextField("");
                    Object configs = new Object[]{"Name: ",name};
                    int r = JOptionPane.showConfirmDialog(null, configs, "Add module", JOptionPane.OK_CANCEL_OPTION);  
                    if (r == JOptionPane.OK_OPTION){
                        DeviceModule d = new DeviceModule(name.getText());
                        DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
                        DefaultMutableTreeNode child3 = new DefaultMutableTreeNode("Name: "+d.name);
                        child.add(child3);
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, element,element.getChildCount());}}});
            p.add(item);
            item = new JMenuItem("Remove Device");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(element);}});
            p.add(item);}
        else if(type == 1){
            item = new JMenuItem("Add Port");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    JTextField name = new JTextField("");
                    JTextField type = new JTextField("");
                    Object configs = new Object[]{"Port: ",name,"Port type: ",type};
                    int r = JOptionPane.showConfirmDialog(null, configs, "Add port", JOptionPane.OK_CANCEL_OPTION);  
                    if (r == JOptionPane.OK_OPTION){
                        DevicePort d = new DevicePort(name.getText(),type.getText());
                        DefaultMutableTreeNode child = new DefaultMutableTreeNode(d);
                        DefaultMutableTreeNode child3 = new DefaultMutableTreeNode("Port type: "+type.getText());
                        child.add(child3);
                        ((DefaultTreeModel)tree.getModel()).insertNodeInto(child, element,element.getChildCount());}}});
            p.add(item);
            item = new JMenuItem("Remove module");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(element);}});
            p.add(item);}
        else{item = new JMenuItem("Remove port");        
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    ((DefaultTreeModel)tree.getModel()).removeNodeFromParent(element);}});
            p.add(item);}
        p.show(this,ev.getX(),ev.getY());}}