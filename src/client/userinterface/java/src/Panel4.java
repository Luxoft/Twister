import javax.swing.JPanel;
import java.awt.Color;
import javax.swing.JTabbedPane;
import java.awt.Dimension;
import java.awt.Toolkit;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.BorderFactory;
import javax.swing.JScrollPane;

import javax.swing.border.TitledBorder;

public class Panel4 extends JPanel{
    DUT dut;
    ConfigFiles config;
    DBConfig dbconfig;
    Emails emails;
    JPanel main;    
    JScrollPane scroll = new JScrollPane();
    

    public Panel4(){
        setLayout(null);
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize(); 
        dut = new DUT();
        config = new ConfigFiles(screenSize,dut);
        dbconfig = new DBConfig();
        emails = new Emails();
        main = new JPanel();
        main.setLayout(null);
        main.setBounds(240,10,(int)screenSize.getWidth()-320,(int)screenSize.getHeight()-320);
        //main.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "TEST"));
        add(main);   
        RoundButton bpaths = new RoundButton("Paths");
        bpaths.setBounds(20,40,200,25);
        bpaths.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                main.removeAll();
                scroll = new JScrollPane(config.paths);
                scroll.setBounds(5,15,main.getWidth()-10,main.getHeight()-20);
                main.add(scroll);
                main.repaint();
                main.revalidate();}});
        add(bpaths);  
        RoundButton bemails = new RoundButton("Email");
        bemails.setBounds(20,70,200,25);
        bemails.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                main.removeAll();
                scroll = new JScrollPane(emails);
                scroll.setBounds(5,15,main.getWidth()-10,main.getHeight()-20);
                main.add(scroll);
                main.repaint();
                main.revalidate();}});
        add(bemails);
        RoundButton database = new RoundButton("Database");
        database.setBounds(20,100,200,25);
        database.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                main.removeAll();
                scroll = new JScrollPane(dbconfig);
                scroll.setBounds(5,15,main.getWidth()-10,main.getHeight()-20);
                main.add(scroll);
                main.repaint();
                main.revalidate();}});
        add(database);
        RoundButton duts = new RoundButton("Device Under Test");
        duts.setBounds(20,130,200,25);
        duts.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                main.removeAll();
                scroll = new JScrollPane(dut.config);
                scroll.setBounds(5,15,main.getWidth()-10,main.getHeight()-20);
                main.add(scroll);
                main.repaint();
                main.revalidate();}});
        add(duts);
        
        
    }}