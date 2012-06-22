/*
 * TextUtilities.java - Utility functions used by the text area classes
 * Copyright (C) 1999 Slava Pestov
 *
 * You may use and modify this package for any purpose. Redistribution is
 * permitted, in both source and binary form, provided that this notice
 * remains intact in all source distributions of this package.
 */

import javax.swing.text.*;

/**
 * Class with several utility functions used by the text area component.
 * @author Slava Pestov
 * @version $Id: TextUtilities.java,v 1.4 1999/12/13 03:40:30 sp Exp $
 */
public class TextUtilities
{
	/**
	 * Returns the offset of the bracket matching the one at the
	 * specified offset of the document, or -1 if the bracket is
	 * unmatched (or if the character is not a bracket).
	 * @param doc The document
	 * @param offset The offset
	 * @exception BadLocationException If an out-of-bounds access
	 * was attempted on the document text
	 */
	public static int findMatchingBracket(Document doc, int offset)
		throws BadLocationException
	{
		if(doc.getLength() == 0)
			return -1;
		char c = doc.getText(offset,1).charAt(0);
		char cprime; 
		boolean direction; 

		switch(c)
		{
		case '(': cprime = ')'; direction = false; break;
		case ')': cprime = '('; direction = true; break;
		case '[': cprime = ']'; direction = false; break;
		case ']': cprime = '['; direction = true; break;
		case '{': cprime = '}'; direction = false; break;
		case '}': cprime = '{'; direction = true; break;
		default: return -1;
		}

		int count;

		
		

		
		if(direction)
		{
			
			
			count = 1;

			
			String text = doc.getText(0,offset);

			
			for(int i = offset - 1; i >= 0; i--)
			{
				
				
				
				
				char x = text.charAt(i);
				if(x == c)
					count++;

				
				
				
				else if(x == cprime)
				{
					if(--count == 0)
						return i;
				}
			}
		}
		else
		{
			
			
			count = 1;

			
			offset++;

			
			int len = doc.getLength() - offset;

			
			String text = doc.getText(offset,len);

			
			for(int i = 0; i < len; i++)
			{
				
				
				
				
				char x = text.charAt(i);

				if(x == c)
					count++;

				
				
				
				else if(x == cprime)
				{
					if(--count == 0)
						return i + offset;
				}
			}
		}

		
		return -1;
	}

	/**
	 * Locates the start of the word at the specified position.
	 * @param line The text
	 * @param pos The position
	 */
	public static int findWordStart(String line, int pos, String noWordSep)
	{
		char ch = line.charAt(pos - 1);

		if(noWordSep == null)
			noWordSep = "";
		boolean selectNoLetter = (!Character.isLetterOrDigit(ch)
			&& noWordSep.indexOf(ch) == -1);

		int wordStart = 0;
		for(int i = pos - 1; i >= 0; i--)
		{
			ch = line.charAt(i);
			if(selectNoLetter ^ (!Character.isLetterOrDigit(ch) &&
				noWordSep.indexOf(ch) == -1))
			{
				wordStart = i + 1;
				break;
			}
		}

		return wordStart;
	}

	/**
	 * Locates the end of the word at the specified position.
	 * @param line The text
	 * @param pos The position
	 */
	public static int findWordEnd(String line, int pos, String noWordSep)
	{
		char ch = line.charAt(pos);

		if(noWordSep == null)
			noWordSep = "";
		boolean selectNoLetter = (!Character.isLetterOrDigit(ch)
			&& noWordSep.indexOf(ch) == -1);

		int wordEnd = line.length();
		for(int i = pos; i < line.length(); i++)  
		{
			ch = line.charAt(i);
			if(selectNoLetter ^ (!Character.isLetterOrDigit(ch) &&
				noWordSep.indexOf(ch) == -1))
			{
				wordEnd = i;
				break;
			}
		}
		return wordEnd;
	}
}
