import java.util.ArrayList;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JTextField;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.Dimension;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.DefaultMutableTreeNode;

public class DevicePort{    
    String portType,port;
    ArrayList <String[]> properties =  new ArrayList <String[]>();
    DevicePort reference;
    
    public DevicePort(String port, String portType){
        reference = this;
        this.port = port;
        this.portType = portType;}
    
    public String toString(){
        return "Port: "+port;}
    
    public void setPort(String port){
        this.port = port;}
        
    public void setPortType(String portType){
        this.portType = portType;}
        
    public void updateInfo(){
        Repository.window.mainpanel.p4.dut.additem.setEnabled(false);
        Repository.window.mainpanel.p4.dut.remitem.setEnabled(true);
        Repository.window.mainpanel.p4.dut.remitem.setText("Remove port");
        Repository.window.mainpanel.p4.dut.temp3 = reference;
        Repository.window.mainpanel.p4.dut.tname3.setText(port);
        Repository.window.mainpanel.p4.dut.tname4.setText(portType);
        updatePropertys();}
        
    public void updatePropertys(){
        Repository.window.mainpanel.p4.dut.properties3.removeAll();
        if(Repository.window.mainpanel.p4.dut.nodetemp3.getChildAt(Repository.window.mainpanel.p4.dut.nodetemp3.getChildCount()-1).isLeaf()){
            while(Repository.window.mainpanel.p4.dut.nodetemp3.getChildCount()>1){
                ((DefaultTreeModel)Repository.window.mainpanel.p4.dut.explorer.tree.getModel()).removeNodeFromParent(((DefaultMutableTreeNode)Repository.window.mainpanel.p4.dut.nodetemp3.getChildAt(1)));}}
        else{
            while(Repository.window.mainpanel.p4.dut.nodetemp3.getChildAt(1).isLeaf()){
                ((DefaultTreeModel)Repository.window.mainpanel.p4.dut.explorer.tree.getModel()).removeNodeFromParent(((DefaultMutableTreeNode)Repository.window.mainpanel.p4.dut.nodetemp3.getChildAt(1)));}}
        for(int i=0;i<properties.size();i++){
            DefaultMutableTreeNode child2 = new DefaultMutableTreeNode(properties.get(i)[0]+" - "+properties.get(i)[1],false);
            if(Repository.window.mainpanel.p4.dut.nodetemp3.getChildAt(Repository.window.mainpanel.p4.dut.nodetemp3.getChildCount()-1).isLeaf()){
                ((DefaultTreeModel)Repository.window.mainpanel.p4.dut.explorer.tree.getModel()).insertNodeInto(child2,Repository.window.mainpanel.p4.dut.nodetemp3,Repository.window.mainpanel.p4.dut.nodetemp3.getChildCount());}
            else{((DefaultTreeModel)Repository.window.mainpanel.p4.dut.explorer.tree.getModel()).insertNodeInto(child2,Repository.window.mainpanel.p4.dut.nodetemp3,1+i);}
            final JButton b = new JButton("remove");
            b.setBounds(280,i*23+18,78,19);
            b.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    properties.remove(Repository.window.mainpanel.p4.dut.properties3.getComponentZOrder(b)/3);
                    updatePropertys();}});
            Repository.window.mainpanel.p4.dut.properties3.add(b);
            final JTextField text1 = new JTextField();
            text1.setText(properties.get(i)[0]);
            text1.setBounds(6,i*23+18,135,25);
            text1.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    properties.get(Repository.window.mainpanel.p4.dut.properties3.getComponentZOrder(text1)/3)[0]=text1.getText();
                    ((DefaultMutableTreeNode)Repository.window.mainpanel.p4.dut.nodetemp3.getChildAt(1+(Repository.window.mainpanel.p4.dut.properties3.getComponentZOrder(text1)/3))).setUserObject(text1.getText()+" - "+properties.get(Repository.window.mainpanel.p4.dut.properties3.getComponentZOrder(text1)/3)[1]);
                    ((DefaultTreeModel)Repository.window.mainpanel.p4.dut.explorer.tree.getModel()).nodeChanged(Repository.window.mainpanel.p4.dut.nodetemp3.getChildAt(1+(Repository.window.mainpanel.p4.dut.properties3.getComponentZOrder(text1)/3)));}});
            final JTextField text2 = new JTextField();
            text2.setText(properties.get(i)[1]);
            text2.setBounds(143,i*23+18,135,25);    
            text2.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    properties.get(Repository.window.mainpanel.p4.dut.properties3.getComponentZOrder(text1)/3)[1]=text2.getText();
                    ((DefaultMutableTreeNode)Repository.window.mainpanel.p4.dut.nodetemp3.getChildAt(1+(Repository.window.mainpanel.p4.dut.properties3.getComponentZOrder(text1)/3))).setUserObject(properties.get(Repository.window.mainpanel.p4.dut.properties3.getComponentZOrder(text1)/3)[0]+" - "+text2.getText());
                    ((DefaultTreeModel)Repository.window.mainpanel.p4.dut.explorer.tree.getModel()).nodeChanged(Repository.window.mainpanel.p4.dut.nodetemp3.getChildAt(1+(Repository.window.mainpanel.p4.dut.properties3.getComponentZOrder(text1)/3)));}});
            Repository.window.mainpanel.p4.dut.properties3.add(text2);
            Repository.window.mainpanel.p4.dut.properties3.add(text1);}
        Repository.window.mainpanel.p4.dut.properties3.setPreferredSize(new Dimension(Repository.window.mainpanel.p4.dut.properties3.getWidth(),properties.size()*23+18));
        Repository.window.mainpanel.p4.dut.properties3.revalidate();
        Repository.window.mainpanel.p4.dut.properties3.repaint();}}