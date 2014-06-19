/*
File: MyCalendar.java ; This file is part of Twister.
Version: 2.004

Copyright (C) 2012-2013 , Luxoft

Authors: Andrei Costachi <acostachi@luxoft.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Locale;

import javax.swing.BorderFactory;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTable;
import javax.swing.border.BevelBorder;
import javax.swing.table.DefaultTableModel;

public class MyCalendar extends JPanel{
	private static final long serialVersionUID = 1L;
	private Calendar calendar;
	public Days days;
	private JLabel left,right;
	private JTable table;
	
	public MyCalendar(Calendar calendar, JTable table){
		this.calendar = calendar;
		this.table = table;
		setLayout(null);
		days = new Days(table);
		calendar.set(Calendar.DAY_OF_MONTH, 1);
		String dayname = new SimpleDateFormat("EEEE",Locale.US).
								format(calendar.getTime()).toLowerCase();
		days.setDays(calendar.getActualMaximum(Calendar.DAY_OF_MONTH),dayname);
		days.setBounds(0, 0, 668, 300);
		add(days);		
	}
}


/*
 * jpanel class used for days 
 * representation in scheduler
 */
class Days extends JPanel{
	private static final long serialVersionUID = 1L;
	private boolean mousein = false;
	private int mouseX, mouseY;
	private int selectedX = -100;
	private int selectedY = -100;
	private int days;
	private int selecteddaynr;
	private ArrayList <HashMap<String,String>> [] schedules;
	private JTable table;
	private String firstday;
	private String [] daynames = {"Monday","Tuesday",
								  "Wednesday","Thursday",
								  "Friday","Saturday","Sunday"};
	
	public int getSelectedDaynr(){
		return selecteddaynr;
	}
	
	public Days(JTable table){
		setLayout(null);
		setBorder(BorderFactory.createBevelBorder(BevelBorder.LOWERED));
		setBackground(Color.WHITE);
		this.table = table;
		addMouseListener(new MouseAdapter(){
			@Override
			public void mouseReleased(MouseEvent arg0) {
				int daynr = getDayNr(arg0);
				selecteddaynr = daynr;
				updateSelectedDay(daynr);
				selectedX = arg0.getX();
				selectedY = arg0.getY();
				repaint();
			}
			
			@Override
			public void mouseEntered(MouseEvent arg0){
				mousein = true;
			}
			
			@Override
			public void mouseExited(MouseEvent arg0){
				mousein = false;
				repaint();
			}
		});
		addMouseMotionListener(new  MouseAdapter() {
			@Override
			public void mouseMoved(MouseEvent arg0) {
				mouseX = arg0.getX();
				mouseY = arg0.getY();
				repaint();
			}
		});
	}
	
	
	/*
	 * convert mouse location to
	 * day nr
	 */
	public int getDayNr(MouseEvent ev){
		int width = getWidth();
		int height = getHeight();
		int dayWidth = width/7;
		int dayHeight = height/5;
		int dayX = (ev.getX()/dayWidth);
		int dayY = (ev.getY()/dayHeight);
		int day;
		if(dayY==0){
			day = dayX+1;
		} else {
			day = dayY*7+dayX+1;
		}
		return day;
	}
	
	
	/*
	 * method to clear schedules from table
	 * and selected day
	 */
	public void clearTable(){
		DefaultTableModel model = ((DefaultTableModel)table.getModel());
		int nr = model.getRowCount();
		for(int i=nr-1;i>-1;i--){
			model.removeRow(0);
		}
		selectedX = -100;
		selectedY = -100;
	}
	
	
	/*
	 * update schedules list on selected day
	 */
	public void updateSelectedDay(int day){
		try{
			ArrayList <HashMap<String, String>>schedule = schedules[day-1];
			clearTable();
			for(HashMap<String,String> map:schedule){
				String date,hour;
				try{
					date = map.get("date-time").split(" ")[0];
					hour = map.get("date-time").split(" ")[1];
				}catch (Exception e){
					date = "";
					hour = map.get("date-time");							
				}
				DefaultTableModel model = ((DefaultTableModel)table.getModel());
				String force;
				if(map.get("force").equals("0")){
					force = "false";
				} else {
					force = "true";
				}
				model.addRow(new Object[]{map.get("project-file"),
									      date,
									      hour,
										  force,
										  map.get("time-limit"),
										  map.get("description"),
										  map.get("user"),
										  map.get("key")});
			}
		} catch (Exception e){}
	}
	
	/*
	 * paint the selected day
	 */
	private void paintSelected(Graphics2D gr){
		int width = getWidth();
		int height = getHeight();
		int dayWidth = width/7;
		int dayHeight = height/5;
		int dayX = (selectedX/dayWidth);
		int dayY = (selectedY/dayHeight);
		gr.setColor(new Color(190,190,200,70));
		if(dayX==0){
			dayX = 2;
		} else if(dayX == 6){
			dayX*=dayWidth;
			dayWidth = width-(6*dayWidth);
		} else {
			dayX*=dayWidth;
		}
		if(dayY==0){
			dayY = 2;
		} else if(dayY == 4){
			dayY*=dayHeight;
			dayHeight = height-(4*dayHeight);			
		} else {
			dayY*= dayHeight;
		}
		gr.fillRect(dayX, dayY, dayWidth, dayHeight);
	}
	
	/*
	 * method to give a visual 
	 * clue of mouse location on calendar
	 */
	private void paintMouseLocation(Graphics2D gr){
		int width = getWidth();
		int height = getHeight();
		int dayWidth = width/7;
		int dayHeight = height/5;
		int dayX = (mouseX/dayWidth);
		int dayY = (mouseY/dayHeight);
		gr.setColor(new Color(240,240,240));
		if(dayX==0){
			dayX = 2;
		} else if(dayX == 6){
			dayX*=dayWidth;
			dayWidth = width-(6*dayWidth);
		} else {
			dayX*=dayWidth;
		}
		if(dayY==0){
			dayY = 2;
		} else if(dayY == 4){
			dayY*=dayHeight;
			dayHeight = height-(4*dayHeight);			
		} else {
			dayY*= dayHeight;
		}
		gr.fillRect(dayX, dayY, dayWidth, dayHeight);
	}
	
	/*
	 * main paint method
	 */
	public void paint(Graphics g){
		super.paint(g);
		Graphics2D gr = (Graphics2D)g;
		gr.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
							RenderingHints.VALUE_ANTIALIAS_ON);
		if(mousein){
			paintMouseLocation(gr);
		}
		paintDays(gr);
		paintSelected(gr);		
		paintLines(gr);
	}
	
	/*
	 * method to split space and draw 
	 * days lines
	 */
	private void paintLines(Graphics2D gr){
		int width = getWidth();
		int height = getHeight();
		int dayWidth = width/7;
		int dayHeight = height/5;
		gr.setColor(new Color(130,130,160));
		for(int i=1;i<7;i++){
			gr.drawLine(dayWidth*i, 1, dayWidth*i, height-2);
		}
		for(int i=1;i<5;i++){
			gr.drawLine(1, dayHeight*i, width-2, dayHeight*i);
		}
	}
	
	/*
	 * method to display the nr of
	 * day in month and the number of chedules
	 */
	private void paintDays(Graphics2D gr){
		int width = getWidth();
		int height = getHeight();
		int dayWidth = width/7;
		int dayHeight = height/5;
		int dayX, dayY;
		int dayindex=0;
		for(int i=0;i<7;i++){
			if(daynames[i].toLowerCase().equals(firstday.toLowerCase())){
				dayindex = i;
			}
		}
		for(int day = 0;day<days;day++){
			dayWidth = width/7;
			dayHeight = height/5;
			dayX=day%7;
			dayY=day/7;
			gr.setColor(new Color(210,210,230));
			if(dayX==0){
				dayX = 2;
			} else if(dayX == 6){
				dayX*=dayWidth;
				dayWidth = width-(6*dayWidth);
			} else {
				dayX*=dayWidth;
			}
			if(dayY==0){
				dayY = 2;
			} else if(dayY == 4){
				dayY*=dayHeight;
				dayHeight = height-(4*dayHeight);			
			} else {
				dayY*= dayHeight;
			}
			gr.fillRect(dayX, dayY, dayWidth, dayHeight/3);
			gr.setColor(new Color(80,80,80));
			gr.setFont(new Font("Bodoni MT", Font.BOLD, 15));
			gr.drawString(day+1+"",dayX+7,dayY+(dayHeight/3)-5);
			gr.setFont(new Font("Bodoni MT", Font.PLAIN, 11));
			int namewidth = gr.getFontMetrics().stringWidth(daynames[dayindex]);
			gr.drawString(daynames[dayindex],dayX+dayWidth-namewidth-6,
							dayY+(dayHeight/3)-3);
			dayindex++;
			if(dayindex>6)dayindex=0;
			int nr = 0;
			try{nr = schedules[day].size();}
			catch(Exception e){}
			if(nr>0){
				gr.setColor(new Color(80,80,80,100));
				gr.setFont(new Font("Bodoni MT", Font.BOLD, 23));
				gr.drawString(nr+"",dayX+(dayWidth/2)-5,
								dayY+(int)(dayHeight*0.75));
			}
		}
	}

	/*
	 * setter for the number of days
	 * in month
	 */
	public void setDays(int days, String firstday) {
		this.days = days;
		this.firstday = firstday;
	}
	
	public void updateSchedules(ArrayList [] schedules){
		this.schedules = schedules;
	}
	
	
}
