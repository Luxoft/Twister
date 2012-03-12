import javax.swing.JPanel;
import java.awt.Color;
import java.awt.event.MouseMotionAdapter;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.Point;
import javax.swing.JLabel;
import javax.swing.BorderFactory;
import javax.swing.border.BevelBorder;
import java.util.ArrayList;
import javax.swing.JTextField;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.Dimension;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.DefaultMutableTreeNode;

public class Device{
    private int X,Y;
    String name= "";
    String description="";
    String id="";
    String vendor="";
    String type="";
    String family="";
    String model="";
    ArrayList <String[]> propertys =  new ArrayList <String[]>();
    ArrayList <DeviceModule> modules =  new ArrayList <DeviceModule>();
    Device reference;
    
    public Device(){reference = this;}
        
    public void updateInfo(){
        Repository.f.p.p4.dut.temp = reference;
        Repository.f.p.p4.dut.tname.setText(name.toString());
        Repository.f.p.p4.dut.ttype.setText(type.toString());
        Repository.f.p.p4.dut.tvendor.setText(vendor.toString());
        Repository.f.p.p4.dut.tmodel.setText(model.toString());
        Repository.f.p.p4.dut.tfamily.setText(family.toString());
        Repository.f.p.p4.dut.tid.setText(id.toString());        
        Repository.f.p.p4.dut.tdescription.setText(description.toString());
        Repository.f.p.p4.dut.propname.setText("");
        Repository.f.p.p4.dut.propvalue.setText("");
        updatePropertys();}
        
    public void updatePropertys(){
        Repository.f.p.p4.dut.propertys.removeAll();
        if(Repository.f.p.p4.dut.nodetemp1.getChildAt(Repository.f.p.p4.dut.nodetemp1.getChildCount()-1).isLeaf()){
            while(Repository.f.p.p4.dut.nodetemp1.getChildCount()>6){
                ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).removeNodeFromParent(((DefaultMutableTreeNode)Repository.f.p.p4.dut.nodetemp1.getChildAt(6)));}}
        else{
            while(Repository.f.p.p4.dut.nodetemp1.getChildAt(6).isLeaf()){
                ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).removeNodeFromParent(((DefaultMutableTreeNode)Repository.f.p.p4.dut.nodetemp1.getChildAt(6)));}}
        for(int i =0;i<propertys.size();i++){
            DefaultMutableTreeNode child2 = new DefaultMutableTreeNode(propertys.get(i)[0]+" - "+propertys.get(i)[1],false);
            if(Repository.f.p.p4.dut.nodetemp1.getChildAt(Repository.f.p.p4.dut.nodetemp1.getChildCount()-1).isLeaf()){
                ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).insertNodeInto(child2,Repository.f.p.p4.dut.nodetemp1,Repository.f.p.p4.dut.nodetemp1.getChildCount());}
            else{
                ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).insertNodeInto(child2,Repository.f.p.p4.dut.nodetemp1,6+i);}
            final JButton b = new JButton("remove");
            b.setBounds(280,i*23+18,78,19);
            b.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    propertys.remove(Repository.f.p.p4.dut.propertys.getComponentZOrder(b)/3);
                    updatePropertys();}});
            Repository.f.p.p4.dut.propertys.add(b);
            final JTextField text1 = new JTextField();
            text1.setText(propertys.get(i)[0]);
            text1.setBounds(6,i*23+18,135,20);
            text1.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    propertys.get(Repository.f.p.p4.dut.propertys.getComponentZOrder(text1)/3)[0]=text1.getText();
                    ((DefaultMutableTreeNode)Repository.f.p.p4.dut.nodetemp1.getChildAt(6+(Repository.f.p.p4.dut.propertys.getComponentZOrder(text1)/3))).setUserObject(text1.getText()+" - "+propertys.get(Repository.f.p.p4.dut.propertys.getComponentZOrder(text1)/3)[1]);
                    ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).nodeChanged(Repository.f.p.p4.dut.nodetemp1.getChildAt(6+(Repository.f.p.p4.dut.propertys.getComponentZOrder(text1)/3)));}});
            final JTextField text2 = new JTextField();
            text2.setText(propertys.get(i)[1]);
            text2.setBounds(143,i*23+18,135,20);    
            text2.addKeyListener(new KeyAdapter(){
                public void keyReleased(KeyEvent ev){
                    propertys.get(Repository.f.p.p4.dut.propertys.getComponentZOrder(text1)/3)[1]=text2.getText();
                    ((DefaultMutableTreeNode)Repository.f.p.p4.dut.nodetemp1.getChildAt(6+(Repository.f.p.p4.dut.propertys.getComponentZOrder(text1)/3))).setUserObject(propertys.get(Repository.f.p.p4.dut.propertys.getComponentZOrder(text1)/3)[0]+" - "+text2.getText());
                    ((DefaultTreeModel)Repository.f.p.p4.dut.explorer.tree.getModel()).nodeChanged(Repository.f.p.p4.dut.nodetemp1.getChildAt(6+(Repository.f.p.p4.dut.propertys.getComponentZOrder(text1)/3)));}});
            Repository.f.p.p4.dut.propertys.add(text2);
            Repository.f.p.p4.dut.propertys.add(text1);}
        Repository.f.p.p4.dut.propertys.setPreferredSize(new Dimension(Repository.f.p.p4.dut.propertys.getWidth(),propertys.size()*23+18));
        Repository.f.p.p4.dut.propertys.revalidate();
        Repository.f.p.p4.dut.propertys.repaint();}
        
    public void setDescription(String description){
        this.description = description;}
        
    public void setID(String id){
        this.id=id;}
        
    public void setVendor(String vendor){
        this.vendor = vendor;}
        
    public void setType(String type){
        this.type=type;}
        
    public String toString(){
        return name.toString();}
        
    public void addModule(DeviceModule module){
        modules.add(module);}
        
    public void setFamily(String family){
        this.family=family;}
    
    public void setModel(String model){
        this.model=model;}
            
    public void setName(String name){
        this.name=name;}}