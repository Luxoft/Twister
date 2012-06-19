import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.WindowConstants;
import javax.swing.JComboBox;
import javax.swing.GroupLayout;
import javax.swing.SwingConstants;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.LayoutStyle;
import java.awt.Component;
import javax.swing.DefaultComboBoxModel;
import com.google.gson.JsonObject;
import java.util.Map.Entry;
import java.util.Iterator;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import com.google.gson.JsonPrimitive;
import javax.swing.JFileChooser;
import javax.swing.JPanel;
import java.awt.Dimension;
import javax.swing.JOptionPane;
import java.awt.Point;

/*
 * Editors window 
 */
public class Editors extends JFrame {
    private JComboBox editorscombo;
    private JButton remove;
    private JButton add;
    private JButton browse;
    private JCheckBox defaultcheck;
    private JLabel jLabel1;
    private JLabel jLabel2;
    private JLabel jLabel3;
    private JLabel jLabel4;
    private JTextField tcommand;
    private JTextField tname;

    public Editors(Point p) {
        initComponents(p);}        
        
    /*
     * editors window initialization
     */
    private void initComponents(Point p) {
        setLocation(p);
        setAlwaysOnTop(true);
        jLabel1 = new JLabel();
        editorscombo = new JComboBox();
        jLabel2 = new JLabel();
        tname = new JTextField();
        jLabel3 = new JLabel();
        tcommand = new JTextField();
        remove = new JButton();
        add = new JButton();
        jLabel4 = new JLabel();
        defaultcheck = new JCheckBox();
        browse = new JButton();
        
        if(Repository.getDefaultEditor().equals(getEditors()[0]))defaultcheck.setSelected(true);
        if(getEditors()[0].equals("Embedded")){
            tname.setEnabled(false);
            remove.setEnabled(false);
            tcommand.setEnabled(false);
            browse.setEnabled(false);}
        
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                String [] editor = getEditor();
                if(editor!=null){
                    Repository.addEditor(editor);
                    editorscombo.addItem(editor[0]);}}});
        
        remove.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                int index = editorscombo.getSelectedIndex();
                Repository.removeEditor(editorscombo.getSelectedItem().toString());
                editorscombo.removeItemAt(index);}});
        
        tname.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                if(!tname.getText().equals(editorscombo.getSelectedItem().toString())){
                    String name = tname.getText();
                    int caretpos = tname.getCaretPosition();
                    int index = editorscombo.getSelectedIndex();
                    if(defaultcheck.isSelected())Repository.setDefaultEditor(name);
                    saveTName(name,editorscombo.getItemAt(index).toString());
                    editorscombo.removeItemAt(index);
                    editorscombo.insertItemAt(name, index);
                    editorscombo.setSelectedIndex(index);
                    tname.requestFocus();
                    tname.setCaretPosition(caretpos);}}});
        
        tcommand.addKeyListener(new KeyAdapter(){
            public void keyReleased(KeyEvent ev){
                saveTCommand(tcommand.getText(),editorscombo.getSelectedItem().toString());}});
        
        defaultcheck.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(defaultcheck.isSelected())Repository.setDefaultEditor(editorscombo.getSelectedItem().toString());
                else Repository.setDefaultEditor("Embedded");}});

        editorscombo.addItemListener(new ItemListener(){
            public void itemStateChanged(ItemEvent evt){
                if(evt.getStateChange() == ItemEvent.SELECTED){
                    if(evt.getItem().toString().equals("Embedded")){
                        tname.setEnabled(false);
                        remove.setEnabled(false);
                        tcommand.setEnabled(false);
                        browse.setEnabled(false);}
                    else{
                        tname.setEnabled(true);
                        remove.setEnabled(true);
                        tcommand.setEnabled(true);
                        browse.setEnabled(true);}
                    if(Repository.getDefaultEditor().equals(evt.getItem().toString())) defaultcheck.setSelected(true);
                    else defaultcheck.setSelected(false);
                    tname.setText(evt.getItem().toString());
                    tcommand.setText(Repository.getEditors().get(evt.getItem().toString()).getAsString());}}});        
        
        browse.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent evnt){
                JFileChooser chooser = new JFileChooser();
                chooser.setDialogTitle("Select editor executable path"); 
                if (chooser.showOpenDialog(Editors.this) == JFileChooser.APPROVE_OPTION) {                    
                    tcommand.setText(chooser.getSelectedFile().getPath());
                    saveTCommand(tcommand.getText(),editorscombo.getSelectedItem().toString());}}});
        
        editorscombo.setModel(new DefaultComboBoxModel(getEditors()));
        editorscombo.setSelectedIndex(0);
        setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);

        tname.setText(getEditors()[0]);
        tcommand.setText(Repository.getEditors().get(getEditors()[0]).getAsString());
        
        jLabel1.setText("Editors");
        jLabel2.setText("Name");
        jLabel3.setText("Command");
        remove.setText("Remove");
        add.setText("Add");
        jLabel4.setText("Default:");
        browse.setText("...");

        GroupLayout layout = new GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel3)
                            .addComponent(jLabel1)
                            .addComponent(jLabel2))
                        .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addGroup(layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                    .addComponent(editorscombo, GroupLayout.PREFERRED_SIZE, 92, GroupLayout.PREFERRED_SIZE)
                                    .addComponent(tname, GroupLayout.PREFERRED_SIZE, 92, GroupLayout.PREFERRED_SIZE))
                                .addGap(18, 18, 18)
                                .addComponent(jLabel4)
                                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                                .addComponent(defaultcheck))
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(tcommand, GroupLayout.DEFAULT_SIZE, 181, Short.MAX_VALUE)
                                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(browse)))
                        .addContainerGap())
                    .addGroup(layout.createSequentialGroup()
                        .addGap(0, 0, Short.MAX_VALUE)
                        .addComponent(add)
                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(remove)
                        .addGap(10, 10, 10)))));
        layout.linkSize(SwingConstants.HORIZONTAL, new Component[] {remove, add});
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.CENTER)
                    .addComponent(jLabel1)
                    .addComponent(editorscombo, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(18, 18, 18)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.CENTER)
                    .addComponent(tname, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel2)
                    .addComponent(jLabel4)
                    .addComponent(defaultcheck))
                .addGap(18, 18, 18)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.CENTER)
                    .addComponent(jLabel3)
                    .addComponent(tcommand, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(browse))
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(add)
                    .addComponent(remove))
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)));
        pack();}
    
    /*
     * redefine editor path
     */
    public void saveTCommand(String command, String element){
        Repository.addEditor(new String[]{element,command});}
        
    /*
     * change editor name
     * name - new name
     * element - the name to be removed
     */
    public void saveTName(String name, String element){
        Repository.addEditor(new String[]{name,Repository.getEditors().get(element).getAsString()});
        Repository.removeEditor(element);}
        
    /*
     * define a new editor 
     * returns name and path of
     * the new editor
     */    
    public String [] getEditor(){
        JPanel p = new JPanel();
        p.setPreferredSize(new Dimension(375,70));
        p.setMaximumSize(new Dimension(375,70));
        p.setLayout(null);       
        JLabel name = new JLabel("Name:");
        name.setBounds(5,10,60,25);
        p.add(name);
        JTextField tname = new JTextField();
        tname.setBounds(65,10,100,25);
        p.add(tname);
        JLabel path = new JLabel("Path:");
        path.setBounds(5,35,60,25);
        p.add(path);
        final JTextField tpath = new JTextField();
        tpath.setBounds(65,35,250,25);
        p.add(tpath);
        JButton browse = new JButton("...");
        browse.setBounds(320,35,50,25);
        browse.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent evnt){
                JFileChooser chooser = new JFileChooser(); 
                chooser.setDialogTitle("Select editor executable path"); 
                if (chooser.showOpenDialog(Editors.this) == JFileChooser.APPROVE_OPTION) {                    
                    tpath.setText(chooser.getSelectedFile().getPath());}}});
        p.add(browse);
        Object[] message = new Object[] {p};
        int r = (Integer)CustomDialog.showDialog(p, JOptionPane.QUESTION_MESSAGE, JOptionPane.OK_CANCEL_OPTION, Editors.this, "Editor", null);
        if(r == JOptionPane.OK_OPTION && tname.getText().length()>0 && tpath.getText().length()>0){
            System.out.println(tname.getText()+" - "+tpath.getText());
            return new String []{tname.getText(),tpath.getText()};}
        else return null;}
   
    /*
     * get editors from
     * repository as an array
     */
    public String[] getEditors(){
        String [] vecresult;
        JsonObject editors = Repository.getEditors();
        int length = editors.entrySet().size();
        if(editors.get("DEFAULT")!=null)vecresult = new String[length-1];
        else vecresult = new String[length];
        int index = 0;
        Entry entry;
        Iterator iter = editors.entrySet().iterator();
        for(int i=0;i<length;i++){                        
            entry = (Entry)iter.next();
            if(entry.getKey().toString().equals("DEFAULT"))continue;
            vecresult[index] = entry.getKey().toString();
            index++;}
        return vecresult;}}