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
    ArrayList <String[]> propertys =  new ArrayList <String[]>();
    DevicePort reference;
    
    public DevicePort(String port, String portType){
        reference = this;
        this.port = port;
        this.portType = portType;}
    
    public String toString(){
        return port;}
    
    public void setPort(String port){
        this.port = port;}
        
    public void setPortType(String portType){
        this.portType = portType;}
        
    public void updateInfo(){
        Repository.f.p.p4.dut.temp3 = reference;
        Repository.f.p.p4.dut.tname3.setText(port);
        Repository.f.p.p4.dut.tname4.setText(portType);
        updatePropertys();}
        
    public void updatePropertys(){
        Repository.f.p.p4.dut.propertys3.removeAll();
        if(Repository.f.p.p4.dut.nodetemp3.getChildAt(Repository.f.p.p4.dut.nodetemp3.getChildCount()-1).isLeaf()){
            while(Repository.f.p.p4.dut.nodetemp3.getChildCount()>1){
                ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).removeNodeFromParent(((DefaultMutableTreeNode)Repository.f.p.p4.dut.nodetemp3.getChildAt(1)));}}
        else{
            while(Repository.f.p.p4.dut.nodetemp3.getChildAt(1).isLeaf()){
                ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).removeNodeFromParent(((DefaultMutableTreeNode)Repository.f.p.p4.dut.nodetemp3.getChildAt(1)));}}
        for(int i=0;i<propertys.size();i++){
            DefaultMutableTreeNode child2 = new DefaultMutableTreeNode(propertys.get(i)[0]+" - "+propertys.get(i)[1],false);
            if(Repository.f.p.p4.dut.nodetemp3.getChildAt(Repository.f.p.p4.dut.nodetemp3.getChildCount()-1).isLeaf()){
                ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).insertNodeInto(child2,Repository.f.p.p4.dut.nodetemp3,Repository.f.p.p4.dut.nodetemp3.getChildCount());}
            else{
                ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).insertNodeInto(child2,Repository.f.p.p4.dut.nodetemp3,1+i);}
            final JButton b = new JButton("remove");
            b.setBounds(280,i*23+18,78,19);
            b.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    propertys.remove(Repository.f.p.p4.dut.propertys3.getComponentZOrder(b)/3);
                    updatePropertys();}});
            Repository.f.p.p4.dut.propertys3.add(b);
            final JTextField text1 = new JTextField();
            text1.setText(propertys.get(i)[0]);
            text1.setBounds(6,i*23+18,135,20);
            text1.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    propertys.get(Repository.f.p.p4.dut.propertys3.getComponentZOrder(text1)/3)[0]=text1.getText();
                    ((DefaultMutableTreeNode)Repository.f.p.p4.dut.nodetemp3.getChildAt(1+(Repository.f.p.p4.dut.propertys3.getComponentZOrder(text1)/3))).setUserObject(text1.getText()+" - "+propertys.get(Repository.f.p.p4.dut.propertys3.getComponentZOrder(text1)/3)[1]);
                    ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).nodeChanged(Repository.f.p.p4.dut.nodetemp3.getChildAt(1+(Repository.f.p.p4.dut.propertys3.getComponentZOrder(text1)/3)));
                
                }});
            final JTextField text2 = new JTextField();
            text2.setText(propertys.get(i)[1]);
            text2.setBounds(143,i*23+18,135,20);    
            text2.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    propertys.get(Repository.f.p.p4.dut.propertys3.getComponentZOrder(text1)/3)[1]=text2.getText();
                    ((DefaultMutableTreeNode)Repository.f.p.p4.dut.nodetemp3.getChildAt(1+(Repository.f.p.p4.dut.propertys3.getComponentZOrder(text1)/3))).setUserObject(propertys.get(Repository.f.p.p4.dut.propertys3.getComponentZOrder(text1)/3)[0]+" - "+text2.getText());
                    ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).nodeChanged(Repository.f.p.p4.dut.nodetemp3.getChildAt(1+(Repository.f.p.p4.dut.propertys3.getComponentZOrder(text1)/3)));
                }});
            Repository.f.p.p4.dut.propertys3.add(text2);
            Repository.f.p.p4.dut.propertys3.add(text1);}
        Repository.f.p.p4.dut.propertys3.setPreferredSize(new Dimension(Repository.f.p.p4.dut.propertys3.getWidth(),propertys.size()*23+18));
        Repository.f.p.p4.dut.propertys3.revalidate();
        Repository.f.p.p4.dut.propertys3.repaint();}
        
        
    }