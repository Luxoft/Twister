import javax.swing.JOptionPane;
import javax.swing.JDialog;
import java.awt.Component;
import javax.swing.Icon;
import javax.swing.JTextField;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.BoxLayout;

/*
 * custom dialog class
 * to implement always on top
 * 
 */
public class CustomDialog{


    /*
     * options presented as buttons 
     */
    public static String showButtons(Component parent, int messagetype ,int optiontype, Icon icon,Object[] options, String title,String message){
        JOptionPane pane = new JOptionPane(message, messagetype, optiontype, icon, options);
        JDialog dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setVisible(true);
        if(pane.getValue()==null){
            dialog.dispose();
            return "NULL";}
        else{
            dialog.dispose();
            return (String)pane.getValue();}}
        
    
    /*
     * used for OK, CANCEL, OPTION
     */
    public static Object showDialog(Object message,int type,int options,Component parent,String title,Icon icon){
        JOptionPane pane = new JOptionPane(message,type,options,icon);
        JDialog dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setVisible(true);
        if(pane.getValue()==null){
            dialog.dispose();
            return -1;}
        else{
            dialog.dispose();
            return pane.getValue();}}
    
    /*
     * used for input dialog
     */
    public static String showInputDialog(int type,int options,Component parent,String title,String text){
        JTextField field = new JTextField();
        JLabel label = new JLabel(text);
        JPanel p = new JPanel();
        p.setLayout(new BoxLayout(p, BoxLayout.Y_AXIS));
        p.add(label);
        p.add(field);
        JOptionPane pane = new JOptionPane(p,type,options);
        JDialog dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setVisible(true);
        if(pane.getValue()==null||(Integer)pane.getValue()==JOptionPane.CANCEL_OPTION){
            dialog.dispose();
            return null;}
        else{
            dialog.dispose();
            return field.getText();}}
    
    /*
     * used to show info
     */
    public static void showInfo(int type,Component parent,String title,String text){
        JLabel label = new JLabel(text);
        JOptionPane pane = new JOptionPane(label,type,JOptionPane.DEFAULT_OPTION);
        JDialog dialog = pane.createDialog(parent, title);
        dialog.setAlwaysOnTop(true);
        dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setVisible(true);}}
