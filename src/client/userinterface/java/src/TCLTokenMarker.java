/*
 * CTokenMarker.java - C token marker
 * Copyright (C) 1998, 1999 Slava Pestov
 *
 * You may use and modify this package for any purpose. Redistribution is
 * permitted, in both source and binary form, provided that this notice
 * remains intact in all source distributions of this package.
 */

import javax.swing.text.Segment;

/**
 * C token marker.
 *
 * @author Slava Pestov
 * @version $Id: TCLTokenMarker.java,v 1.34 1999/12/13 03:40:29 sp Exp $
 */
public class TCLTokenMarker extends TokenMarker
{
	public TCLTokenMarker()
	{
		this(true,getKeywords());
	}

	public TCLTokenMarker(boolean cpp, KeywordMap keywords)
	{
		this.cpp = cpp;
		this.keywords = keywords;
	}

	public byte markTokensImpl(byte token, Segment line, int lineIndex)
	{
		char[] array = line.array;
		int offset = line.offset;
		lastOffset = offset;
		lastKeyword = offset;
		int length = line.count + offset;
		boolean backslash = false;

loop:		for(int i = offset; i < length; i++)
		{
			int i1 = (i+1);

			char c = array[i];
			if(c == '\\')
			{
				backslash = !backslash;
				continue;
			}

			switch(token)
			{
			case Token.NULL:
				switch(c)
				{
				case '#':
					if(backslash)
						backslash = false;
					else if(cpp)
					{
						if(doKeyword(line,i,c))
							break;
						addToken(i - lastOffset,token);
						addToken(length - i,Token.KEYWORD2);
						lastOffset = lastKeyword = length;
						break loop;
					}
					break;
				case '"':
					doKeyword(line,i,c);
					if(backslash)
						backslash = false;
					else
					{
						addToken(i - lastOffset,token);
						token = Token.LITERAL1;
						lastOffset = lastKeyword = i;
					}
					break;
				case '\'':
					doKeyword(line,i,c);
					if(backslash)
						backslash = false;
					else
					{
						addToken(i - lastOffset,token);
						token = Token.LITERAL2;
						lastOffset = lastKeyword = i;
					}
					break;
				case ':':
					if(lastKeyword == offset)
					{
						if(doKeyword(line,i,c))
							break;
						backslash = false;
						addToken(i1 - lastOffset,Token.LABEL);
						lastOffset = lastKeyword = i1;
					}
					else if(doKeyword(line,i,c))
						break;
					break;
				case '/':
					backslash = false;
					doKeyword(line,i,c);
					if(length - i > 1)
					{
						switch(array[i1])
						{
						case '*':
							addToken(i - lastOffset,token);
							lastOffset = lastKeyword = i;
							if(length - i > 2 && array[i+2] == '*')
								token = Token.COMMENT2;
							else
								token = Token.COMMENT1;
							break;
						case '/':
							addToken(i - lastOffset,token);
							addToken(length - i,Token.COMMENT1);
							lastOffset = lastKeyword = length;
							break loop;
						}
					}
					break;
				default:
					backslash = false;
					if(!Character.isLetterOrDigit(c)
						&& c != '_')
						doKeyword(line,i,c);
					break;
				}
				break;
			case Token.COMMENT1:
			case Token.COMMENT2:
				backslash = false;
				if(c == '*' && length - i > 1)
				{
					if(array[i1] == '/')
					{
						i++;
						addToken((i+1) - lastOffset,token);
						token = Token.NULL;
						lastOffset = lastKeyword = i+1;
					}
				}
				break;
			case Token.LITERAL1:
				if(backslash)
					backslash = false;
				else if(c == '"')
				{
					addToken(i1 - lastOffset,token);
					token = Token.NULL;
					lastOffset = lastKeyword = i1;
				}
				break;
			case Token.LITERAL2:
				if(backslash)
					backslash = false;
				else if(c == '\'')
				{
					addToken(i1 - lastOffset,Token.LITERAL1);
					token = Token.NULL;
					lastOffset = lastKeyword = i1;
				}
				break;
			default:
				throw new InternalError("Invalid state: "
					+ token);
			}
		}

		if(token == Token.NULL)
			doKeyword(line,length,'\0');

		switch(token)
		{
		case Token.LITERAL1:
		case Token.LITERAL2:
			addToken(length - lastOffset,Token.INVALID);
			token = Token.NULL;
			break;
		case Token.KEYWORD2:
			addToken(length - lastOffset,token);
			if(!backslash)
				token = Token.NULL;
		default:
			addToken(length - lastOffset,token);
			break;
		}

		return token;
	}

	public static KeywordMap getKeywords()
	{
		if(cKeywords == null)
		{
			cKeywords = new KeywordMap(false);			
			cKeywords.add("append",Token.KEYWORD1);
            cKeywords.add("array",Token.KEYWORD1);
            cKeywords.add("concat",Token.KEYWORD1);
            cKeywords.add("console",Token.KEYWORD1);
            cKeywords.add("eval",Token.KEYWORD1);
            cKeywords.add("expr",Token.KEYWORD1);
            cKeywords.add("format",Token.KEYWORD1);
            cKeywords.add("global",Token.KEYWORD1);
            cKeywords.add("set",Token.KEYWORD1);
            cKeywords.add("trace",Token.KEYWORD1);
            cKeywords.add("unset",Token.KEYWORD1);
            cKeywords.add("upvar",Token.KEYWORD1);
            cKeywords.add("join",Token.KEYWORD1);
            cKeywords.add("lappend",Token.KEYWORD1);
            cKeywords.add("lindex",Token.KEYWORD1);
            cKeywords.add("linsert",Token.KEYWORD1);
            cKeywords.add("list",Token.KEYWORD1);
            cKeywords.add("llength",Token.KEYWORD1);
            cKeywords.add("lrange",Token.KEYWORD1);
            cKeywords.add("lreplace",Token.KEYWORD1);
            cKeywords.add("lsearch",Token.KEYWORD1);
            cKeywords.add("lsort",Token.KEYWORD1);
            cKeywords.add("split",Token.KEYWORD1);
            cKeywords.add("scan",Token.KEYWORD1);
            cKeywords.add("string",Token.KEYWORD1);
            cKeywords.add("regexp",Token.KEYWORD1);
            cKeywords.add("regsub",Token.KEYWORD1);
            cKeywords.add("if",Token.KEYWORD1);
            cKeywords.add("else",Token.KEYWORD1);
            cKeywords.add("elseif",Token.KEYWORD1);
            cKeywords.add("switch",Token.KEYWORD1);
            cKeywords.add("for",Token.KEYWORD1);
            cKeywords.add("foreach",Token.KEYWORD1);
            cKeywords.add("while",Token.KEYWORD1);
            cKeywords.add("break",Token.KEYWORD1);
            cKeywords.add("continue",Token.KEYWORD1);
            cKeywords.add("proc",Token.KEYWORD1);
            cKeywords.add("return",Token.KEYWORD1);
            cKeywords.add("source",Token.KEYWORD1);
            cKeywords.add("unknown",Token.KEYWORD1);
            cKeywords.add("uplevel",Token.KEYWORD1);
            cKeywords.add("cd",Token.KEYWORD1);
            cKeywords.add("close",Token.KEYWORD1);
            cKeywords.add("eof",Token.KEYWORD1);
            cKeywords.add("file",Token.KEYWORD1);
            cKeywords.add("flush",Token.KEYWORD1);
            cKeywords.add("gets",Token.KEYWORD1);
            cKeywords.add("glob",Token.KEYWORD1);
            cKeywords.add("open",Token.KEYWORD1);
            cKeywords.add("read",Token.KEYWORD1);
            cKeywords.add("puts",Token.KEYWORD1);
            cKeywords.add("pwd",Token.KEYWORD1);
            cKeywords.add("seek",Token.KEYWORD1);
            cKeywords.add("tell",Token.KEYWORD1);
            cKeywords.add("catch",Token.KEYWORD1);
            cKeywords.add("error",Token.KEYWORD1);
            cKeywords.add("exec",Token.KEYWORD1);
            cKeywords.add("pid",Token.KEYWORD1);
            cKeywords.add("after",Token.KEYWORD1);
            cKeywords.add("time",Token.KEYWORD1);
            cKeywords.add("exit",Token.KEYWORD1);
            cKeywords.add("history",Token.KEYWORD1);
            cKeywords.add("rename",Token.KEYWORD1);
            cKeywords.add("info",Token.KEYWORD1);
            cKeywords.add("ceil",Token.KEYWORD1);
            cKeywords.add("floor",Token.KEYWORD1);
            cKeywords.add("round",Token.KEYWORD1);
            cKeywords.add("incr",Token.KEYWORD1);
            cKeywords.add("abs",Token.KEYWORD1);
            cKeywords.add("acos",Token.KEYWORD1);
            cKeywords.add("cos",Token.KEYWORD1);
            cKeywords.add("cosh",Token.KEYWORD1);
            cKeywords.add("asin",Token.KEYWORD1);
            cKeywords.add("sin",Token.KEYWORD1);
            cKeywords.add("sinh",Token.KEYWORD1);
            cKeywords.add("atan",Token.KEYWORD1);
            cKeywords.add("atan2",Token.KEYWORD1);
            cKeywords.add("tan",Token.KEYWORD1);
            cKeywords.add("tanh",Token.KEYWORD1);
            cKeywords.add("log",Token.KEYWORD1);
            cKeywords.add("log10",Token.KEYWORD1);
            cKeywords.add("fmod",Token.KEYWORD1);
            cKeywords.add("pow",Token.KEYWORD1);
            cKeywords.add("hypot",Token.KEYWORD1);
            cKeywords.add("sqrt",Token.KEYWORD1);
            cKeywords.add("double",Token.KEYWORD1);
            cKeywords.add("int",Token.KEYWORD1);
            cKeywords.add("bgerror",Token.KEYWORD1);
            cKeywords.add("binary",Token.KEYWORD1);
            cKeywords.add("clock",Token.KEYWORD1);
            cKeywords.add("dde",Token.KEYWORD1);
            cKeywords.add("encoding",Token.KEYWORD1);
            cKeywords.add("fblocked",Token.KEYWORD1);
            cKeywords.add("fconfigure",Token.KEYWORD1);
            cKeywords.add("fcopy",Token.KEYWORD1);
            cKeywords.add("fileevent",Token.KEYWORD1);
            cKeywords.add("filename",Token.KEYWORD1);
            cKeywords.add("http",Token.KEYWORD1);
            cKeywords.add("interp",Token.KEYWORD1);
            cKeywords.add("load",Token.KEYWORD1);
            cKeywords.add("lset",Token.KEYWORD1);
            cKeywords.add("memory",Token.KEYWORD1);
            cKeywords.add("msgcat",Token.KEYWORD1);
            cKeywords.add("namespace",Token.KEYWORD1);
            cKeywords.add("package",Token.KEYWORD1);
            cKeywords.add("pkg::create",Token.KEYWORD1);
            cKeywords.add("pkg_mkIndex",Token.KEYWORD1);
            cKeywords.add("registry",Token.KEYWORD1);
            cKeywords.add("resource",Token.KEYWORD1);
            cKeywords.add("socket",Token.KEYWORD1);
            cKeywords.add("subst",Token.KEYWORD1);
            cKeywords.add("update",Token.KEYWORD1);
            cKeywords.add("variable",Token.KEYWORD1);
            cKeywords.add("vwait",Token.KEYWORD1);
            cKeywords.add("auto_execok",Token.KEYWORD1);
            cKeywords.add("auto_import",Token.KEYWORD1);
            cKeywords.add("auto_load",Token.KEYWORD1);
            cKeywords.add("auto_mkindex",Token.KEYWORD1);
            cKeywords.add("auto_mkindex_old",Token.KEYWORD1);
            cKeywords.add("auto_qualify",Token.KEYWORD1);
            cKeywords.add("auto_reset",Token.KEYWORD1);
            cKeywords.add("parray",Token.KEYWORD1);
            cKeywords.add("tcl_endOfWord",Token.KEYWORD1);
            cKeywords.add("tcl_findLibrary",Token.KEYWORD1);
            cKeywords.add("tcl_startOfNextWord",Token.KEYWORD1);
            cKeywords.add("tcl_startOfPreviousWord",Token.KEYWORD1);
            cKeywords.add("tcl_wordBreakAfter",Token.KEYWORD1);
            cKeywords.add("tcl_wordBreakBefore",Token.KEYWORD1);
            cKeywords.add("bind",Token.KEYWORD2);
            cKeywords.add("button",Token.KEYWORD2);
            cKeywords.add("canvas",Token.KEYWORD2);
            cKeywords.add("checkbutton",Token.KEYWORD2);
            cKeywords.add("destroy",Token.KEYWORD2);
            cKeywords.add("entry",Token.KEYWORD2);
            cKeywords.add("focus",Token.KEYWORD2);
            cKeywords.add("frame",Token.KEYWORD2);
            cKeywords.add("grab",Token.KEYWORD2);
            cKeywords.add("image",Token.KEYWORD2);
            cKeywords.add("label",Token.KEYWORD2);
            cKeywords.add("listbox",Token.KEYWORD2);
            cKeywords.add("lower",Token.KEYWORD2);
            cKeywords.add("menu",Token.KEYWORD2);
            cKeywords.add("menubutton",Token.KEYWORD2);
            cKeywords.add("message",Token.KEYWORD2);
            cKeywords.add("option",Token.KEYWORD2);
            cKeywords.add("pack",Token.KEYWORD2);
            cKeywords.add("placer",Token.KEYWORD2);
            cKeywords.add("radiobutton",Token.KEYWORD2);
            cKeywords.add("raise",Token.KEYWORD2);
            cKeywords.add("scale",Token.KEYWORD2);
            cKeywords.add("scrollbar",Token.KEYWORD2);
            cKeywords.add("selection",Token.KEYWORD2);
            cKeywords.add("send",Token.KEYWORD2);
            cKeywords.add("text",Token.KEYWORD2);
            cKeywords.add("tk",Token.KEYWORD2);
            cKeywords.add("tkerror",Token.KEYWORD2);
            cKeywords.add("tkwait",Token.KEYWORD2);
            cKeywords.add("toplevel",Token.KEYWORD2);
            cKeywords.add("update",Token.KEYWORD2);
            cKeywords.add("winfo",Token.KEYWORD2);
            cKeywords.add("wm",Token.KEYWORD2);
            cKeywords.add("debug",Token.KEYWORD2);
            cKeywords.add("disconnect",Token.KEYWORD2);
            cKeywords.add("exp_continue",Token.KEYWORD2);
            cKeywords.add("exp_internal",Token.KEYWORD2);
            cKeywords.add("exp_open",Token.KEYWORD2);
            cKeywords.add("exp_pid",Token.KEYWORD2);
            cKeywords.add("exp_version",Token.KEYWORD2);
            cKeywords.add("expect",Token.KEYWORD2);
            cKeywords.add("expect_after",Token.KEYWORD2);
            cKeywords.add("expect_background",Token.KEYWORD2);
            cKeywords.add("expect_before",Token.KEYWORD2);
            cKeywords.add("expect_tty",Token.KEYWORD2);
            cKeywords.add("expect_user",Token.KEYWORD2);
            cKeywords.add("fork",Token.KEYWORD2);
            cKeywords.add("inter_return",Token.KEYWORD2);
            cKeywords.add("interact",Token.KEYWORD2);
            cKeywords.add("interpreter",Token.KEYWORD2);
            cKeywords.add("log_file",Token.KEYWORD2);
            cKeywords.add("log_user",Token.KEYWORD2);
            cKeywords.add("match_max",Token.KEYWORD2);
            cKeywords.add("overlay",Token.KEYWORD2);
            cKeywords.add("parity",Token.KEYWORD2);
            cKeywords.add("promptl",Token.KEYWORD2);
            cKeywords.add("prompt2",Token.KEYWORD2);
            cKeywords.add("remove_nulls",Token.KEYWORD2);
            cKeywords.add("send_error ",Token.KEYWORD2);
            cKeywords.add("send_log",Token.KEYWORD2);
            cKeywords.add("send_tty",Token.KEYWORD2);
            cKeywords.add("send_user",Token.KEYWORD2);
            cKeywords.add("sleep",Token.KEYWORD2);
            cKeywords.add("spawn",Token.KEYWORD2);
            cKeywords.add("strace",Token.KEYWORD2);
            cKeywords.add("stty",Token.KEYWORD2);
            cKeywords.add("system",Token.KEYWORD2);
            cKeywords.add("timestamp",Token.KEYWORD2);
            cKeywords.add("trap",Token.KEYWORD2);
            cKeywords.add("wait",Token.KEYWORD2);
			cKeywords.add("full_buffer",Token.KEYWORD3);
            cKeywords.add("timeout",Token.KEYWORD3);
            cKeywords.add("argv0",Token.KEYWORD3);
            cKeywords.add("argv",Token.KEYWORD3);
            cKeywords.add("argc",Token.KEYWORD3);
            cKeywords.add("tk_version",Token.KEYWORD3);
            cKeywords.add("tk_library",Token.KEYWORD3);
            cKeywords.add("tk_strictMotif",Token.KEYWORD3);
            cKeywords.add("env",Token.KEYWORD3);
            cKeywords.add("errorCode",Token.KEYWORD3);
            cKeywords.add("errorInfo",Token.KEYWORD3);
            cKeywords.add("geometry",Token.KEYWORD3);
            cKeywords.add("tcl_library",Token.KEYWORD3);
            cKeywords.add("tcl_patchLevel",Token.KEYWORD3);
            cKeywords.add("tcl_pkgPath",Token.KEYWORD3);
            cKeywords.add("tcl_platform",Token.KEYWORD3);
            cKeywords.add("tcl_precision",Token.KEYWORD3);
            cKeywords.add("tcl_rcFileName",Token.KEYWORD3);
            cKeywords.add("tcl_rcRsrcName",Token.KEYWORD3);
            cKeywords.add("tcl_traceCompile",Token.KEYWORD3);
            cKeywords.add("tcl_traceExec",Token.KEYWORD3);
            cKeywords.add("tcl_wordchars",Token.KEYWORD3);
            cKeywords.add("tcl_nonwordchars",Token.KEYWORD3);
            cKeywords.add("tcl_version",Token.KEYWORD3);
            cKeywords.add("tcl_interactive",Token.KEYWORD3);
            cKeywords.add("exact",Token.KEYWORD3);
            cKeywords.add("all",Token.KEYWORD3);
            cKeywords.add("indices",Token.KEYWORD3);
            cKeywords.add("nocase",Token.KEYWORD3);
            cKeywords.add("nocomplain",Token.KEYWORD3);
            cKeywords.add("nonewline",Token.KEYWORD3);
            cKeywords.add("code",Token.KEYWORD3);
            cKeywords.add("errorinfo",Token.KEYWORD3);
            cKeywords.add("errorcode",Token.KEYWORD3);
            cKeywords.add("atime",Token.KEYWORD3);
            cKeywords.add("anymore",Token.KEYWORD3);
            cKeywords.add("args",Token.KEYWORD3);
            cKeywords.add("body",Token.KEYWORD3);
            cKeywords.add("compare",Token.KEYWORD3);
            cKeywords.add("cmdcount",Token.KEYWORD3);
            cKeywords.add("commands",Token.KEYWORD3);
            cKeywords.add("ctime",Token.KEYWORD3);
            cKeywords.add("current",Token.KEYWORD3);
            cKeywords.add("default",Token.KEYWORD3);
            cKeywords.add("dev",Token.KEYWORD3);
            cKeywords.add("dirname",Token.KEYWORD3);
            cKeywords.add("donesearch",Token.KEYWORD3);
            cKeywords.add("errorinfo",Token.KEYWORD3);
            cKeywords.add("executable",Token.KEYWORD3);
            cKeywords.add("extension",Token.KEYWORD3);
            cKeywords.add("first",Token.KEYWORD3);
            cKeywords.add("globals",Token.KEYWORD3);
            cKeywords.add("gid",Token.KEYWORD3);
            cKeywords.add("index",Token.KEYWORD3);
            cKeywords.add("ino",Token.KEYWORD3);
            cKeywords.add("isdirectory",Token.KEYWORD3);
            cKeywords.add("isfile",Token.KEYWORD3);
            cKeywords.add("keep",Token.KEYWORD3);
            cKeywords.add("last",Token.KEYWORD3);
            cKeywords.add("level",Token.KEYWORD3);
            cKeywords.add("length",Token.KEYWORD3);
            cKeywords.add("library",Token.KEYWORD3);
            cKeywords.add("locals",Token.KEYWORD3);
            cKeywords.add("lstat",Token.KEYWORD3);
            cKeywords.add("match",Token.KEYWORD3);
            cKeywords.add("mode",Token.KEYWORD3);
            cKeywords.add("mtime",Token.KEYWORD3);
            cKeywords.add("names",Token.KEYWORD3);
            cKeywords.add("nextelement",Token.KEYWORD3);
            cKeywords.add("nextid",Token.KEYWORD3);
            cKeywords.add("nlink",Token.KEYWORD3);
            cKeywords.add("none",Token.KEYWORD3);
            cKeywords.add("procs",Token.KEYWORD3);
            cKeywords.add("owned",Token.KEYWORD3);
            cKeywords.add("range",Token.KEYWORD3);
            cKeywords.add("readable",Token.KEYWORD3);
            cKeywords.add("readlink",Token.KEYWORD3);
            cKeywords.add("redo",Token.KEYWORD3);
            cKeywords.add("release",Token.KEYWORD3);
            cKeywords.add("rootname",Token.KEYWORD3);
            cKeywords.add("script",Token.KEYWORD3);
            cKeywords.add("show",Token.KEYWORD3);
            cKeywords.add("size",Token.KEYWORD3);
            cKeywords.add("startsearch",Token.KEYWORD3);
            cKeywords.add("stat",Token.KEYWORD3);
            cKeywords.add("status",Token.KEYWORD3);
            cKeywords.add("substitute",Token.KEYWORD3);
            cKeywords.add("tail",Token.KEYWORD3);
            cKeywords.add("tclversion",Token.KEYWORD3);
            cKeywords.add("tolower",Token.KEYWORD3);
            cKeywords.add("toupper",Token.KEYWORD3);
            cKeywords.add("trim",Token.KEYWORD3);
            cKeywords.add("trimleft",Token.KEYWORD3);
            cKeywords.add("trimright",Token.KEYWORD3);
            cKeywords.add("type",Token.KEYWORD3);
            cKeywords.add("uid",Token.KEYWORD3);
            cKeywords.add("variable",Token.KEYWORD3);
            cKeywords.add("vars",Token.KEYWORD3);
            cKeywords.add("vdelete",Token.KEYWORD3);
            cKeywords.add("vinfo",Token.KEYWORD3);
            cKeywords.add("visibility",Token.KEYWORD3);
            cKeywords.add("window",Token.KEYWORD3);
            cKeywords.add("writable",Token.KEYWORD3);
            cKeywords.add("accelerator",Token.KEYWORD3);
            cKeywords.add("activeforeground",Token.KEYWORD3);
            cKeywords.add("activebackground",Token.KEYWORD3);
            cKeywords.add("anchor",Token.KEYWORD3);
            cKeywords.add("aspect",Token.KEYWORD3);
            cKeywords.add("background",Token.KEYWORD3);
            cKeywords.add("before",Token.KEYWORD3);
            cKeywords.add("bg",Token.KEYWORD3);
            cKeywords.add("borderwidth",Token.KEYWORD3);
            cKeywords.add("bd",Token.KEYWORD3);
            cKeywords.add("bitmap",Token.KEYWORD3);
            cKeywords.add("command",Token.KEYWORD3);
            cKeywords.add("cursor",Token.KEYWORD3);
            cKeywords.add("default",Token.KEYWORD3);
            cKeywords.add("expand",Token.KEYWORD3);
            cKeywords.add("family",Token.KEYWORD3);
            cKeywords.add("fg",Token.KEYWORD3);
            cKeywords.add("fill",Token.KEYWORD3);
            cKeywords.add("font",Token.KEYWORD3);
            cKeywords.add("force",Token.KEYWORD3);
            cKeywords.add("foreground",Token.KEYWORD3);
            cKeywords.add("from",Token.KEYWORD3);
            cKeywords.add("height",Token.KEYWORD3);
            cKeywords.add("icon",Token.KEYWORD3);
            cKeywords.add("question",Token.KEYWORD3);
            cKeywords.add("warning",Token.KEYWORD3);
            cKeywords.add("in",Token.KEYWORD3);
            cKeywords.add("ipadx",Token.KEYWORD3);
            cKeywords.add("ipady",Token.KEYWORD3);
            cKeywords.add("justify",Token.KEYWORD3);
            cKeywords.add("left",Token.KEYWORD3);
            cKeywords.add("center",Token.KEYWORD3);
            cKeywords.add("right",Token.KEYWORD3);
            cKeywords.add("length",Token.KEYWORD3);
            cKeywords.add("padx",Token.KEYWORD3);
            cKeywords.add("pady",Token.KEYWORD3);
            cKeywords.add("offvalue",Token.KEYWORD3);
            cKeywords.add("onvalue",Token.KEYWORD3);
            cKeywords.add("orient",Token.KEYWORD3);
            cKeywords.add("horizontal",Token.KEYWORD3);
            cKeywords.add("vertical",Token.KEYWORD3);
            cKeywords.add("outline",Token.KEYWORD3);
            cKeywords.add("oversrike",Token.KEYWORD3);
            cKeywords.add("relief",Token.KEYWORD3);
            cKeywords.add("raised",Token.KEYWORD3);
            cKeywords.add("sunken",Token.KEYWORD3);
            cKeywords.add("flat",Token.KEYWORD3);
            cKeywords.add("groove",Token.KEYWORD3);
            cKeywords.add("ridge",Token.KEYWORD3);
            cKeywords.add("solid",Token.KEYWORD3);
            cKeywords.add("screen",Token.KEYWORD3);
            cKeywords.add("selectbackground",Token.KEYWORD3);
            cKeywords.add("selectforeground",Token.KEYWORD3);
            cKeywords.add("setgrid",Token.KEYWORD3);
            cKeywords.add("side",Token.KEYWORD3);
            cKeywords.add("size",Token.KEYWORD3);
            cKeywords.add("slant",Token.KEYWORD3);
            cKeywords.add("left",Token.KEYWORD3);
            cKeywords.add("right",Token.KEYWORD3);
            cKeywords.add("top",Token.KEYWORD3);
            cKeywords.add("bottom",Token.KEYWORD3);
            cKeywords.add("spacing1",Token.KEYWORD3);
            cKeywords.add("spacing2",Token.KEYWORD3);
            cKeywords.add("spacing3",Token.KEYWORD3);
            cKeywords.add("state",Token.KEYWORD3);
            cKeywords.add("stipple",Token.KEYWORD3);
            cKeywords.add("takefocus",Token.KEYWORD3);
            cKeywords.add("tearoff",Token.KEYWORD3);
            cKeywords.add("textvariable",Token.KEYWORD3);
            cKeywords.add("title",Token.KEYWORD3);
            cKeywords.add("to",Token.KEYWORD3);
            cKeywords.add("type",Token.KEYWORD3);
            cKeywords.add("abortretryignore",Token.KEYWORD3);
            cKeywords.add("ok",Token.KEYWORD3);
            cKeywords.add("okcancel",Token.KEYWORD3);
            cKeywords.add("retrycancel",Token.KEYWORD3);
            cKeywords.add("yesno",Token.KEYWORD3);
            cKeywords.add("yesnocancel",Token.KEYWORD3);
            cKeywords.add("underline",Token.KEYWORD3);
            cKeywords.add("value",Token.KEYWORD3);
            cKeywords.add("variable",Token.KEYWORD3);
            cKeywords.add("weight",Token.KEYWORD3);
            cKeywords.add("width",Token.KEYWORD3);
            cKeywords.add("xscrollcommand",Token.KEYWORD3);
            cKeywords.add("yscrollcommand",Token.KEYWORD3);
            cKeywords.add("active",Token.KEYWORD3);
            cKeywords.add("add",Token.KEYWORD3);
            cKeywords.add("arc",Token.KEYWORD3);
            cKeywords.add("aspect",Token.KEYWORD3);
            cKeywords.add("bitmap",Token.KEYWORD3);
            cKeywords.add("cascade",Token.KEYWORD3);
            cKeywords.add("cget",Token.KEYWORD3);
            cKeywords.add("children",Token.KEYWORD3);
            cKeywords.add("class",Token.KEYWORD3);
            cKeywords.add("clear",Token.KEYWORD3);
            cKeywords.add("client",Token.KEYWORD3);
            cKeywords.add("create",Token.KEYWORD3);
            cKeywords.add("colormodel",Token.KEYWORD3);
            cKeywords.add("command",Token.KEYWORD3);
            cKeywords.add("configure",Token.KEYWORD3);
            cKeywords.add("deiconify",Token.KEYWORD3);
            cKeywords.add("delete",Token.KEYWORD3);
            cKeywords.add("disabled",Token.KEYWORD3);
            cKeywords.add("exists",Token.KEYWORD3);
            cKeywords.add("focusmodel",Token.KEYWORD3);
            cKeywords.add("flash",Token.KEYWORD3);
            cKeywords.add("forget",Token.KEYWORD3);
            cKeywords.add("geometry",Token.KEYWORD3);
            cKeywords.add("get",Token.KEYWORD3);
            cKeywords.add("group",Token.KEYWORD3);
            cKeywords.add("handle",Token.KEYWORD3);
            cKeywords.add("iconbitmap",Token.KEYWORD3);
            cKeywords.add("iconify",Token.KEYWORD3);
            cKeywords.add("iconmask",Token.KEYWORD3);
            cKeywords.add("iconname",Token.KEYWORD3);
            cKeywords.add("iconposition",Token.KEYWORD3);
            cKeywords.add("iconwindow",Token.KEYWORD3);
            cKeywords.add("idletasks",Token.KEYWORD3);
            cKeywords.add("insert",Token.KEYWORD3);
            cKeywords.add("interps",Token.KEYWORD3);
            cKeywords.add("itemconfigure",Token.KEYWORD3);
            cKeywords.add("invoke",Token.KEYWORD3);
            cKeywords.add("line",Token.KEYWORD3);
            cKeywords.add("mark",Token.KEYWORD3);
            cKeywords.add("maxsize",Token.KEYWORD3);
            cKeywords.add("minsize",Token.KEYWORD3);
            cKeywords.add("move",Token.KEYWORD3);
            cKeywords.add("name",Token.KEYWORD3);
            cKeywords.add("normal",Token.KEYWORD3);
            cKeywords.add("overrideredirect",Token.KEYWORD3);
            cKeywords.add("oval",Token.KEYWORD3);
            cKeywords.add("own",Token.KEYWORD3);
            cKeywords.add("photo",Token.KEYWORD3);
            cKeywords.add("polygon",Token.KEYWORD3);
            cKeywords.add("positionfrom",Token.KEYWORD3);
            cKeywords.add("propagate",Token.KEYWORD3);
            cKeywords.add("protocol",Token.KEYWORD3);
            cKeywords.add("ranges",Token.KEYWORD3);
            cKeywords.add("rectangle",Token.KEYWORD3);
            cKeywords.add("remove",Token.KEYWORD3);
            cKeywords.add("resizable",Token.KEYWORD3);
            cKeywords.add("separator",Token.KEYWORD3);
            cKeywords.add("slaves",Token.KEYWORD3);
            cKeywords.add("sizefrom",Token.KEYWORD3);
            cKeywords.add("state",Token.KEYWORD3);
            cKeywords.add("tag",Token.KEYWORD3);
            cKeywords.add("title",Token.KEYWORD3);
            cKeywords.add("transient",Token.KEYWORD3);
            cKeywords.add("window",Token.KEYWORD3);
            cKeywords.add("withdraw",Token.KEYWORD3);
            cKeywords.add("xview",Token.KEYWORD3);
            cKeywords.add("yview",Token.KEYWORD3);
            cKeywords.add("Activate",Token.KEYWORD3);
            cKeywords.add("Alt",Token.KEYWORD3);
            cKeywords.add("Any",Token.KEYWORD3);
            cKeywords.add("B1",Token.KEYWORD3);
            cKeywords.add("B2",Token.KEYWORD3);
            cKeywords.add("B3",Token.KEYWORD3);
            cKeywords.add("Button1",Token.KEYWORD3);
            cKeywords.add("Button2",Token.KEYWORD3);
            cKeywords.add("Button3",Token.KEYWORD3);
            cKeywords.add("ButtonPress",Token.KEYWORD3);
            cKeywords.add("ButtonRelease",Token.KEYWORD3);
            cKeywords.add("Double",Token.KEYWORD3);
            cKeywords.add("Circulate",Token.KEYWORD3);
            cKeywords.add("Colormap",Token.KEYWORD3);
            cKeywords.add("Configure",Token.KEYWORD3);
            cKeywords.add("Control",Token.KEYWORD3);
            cKeywords.add("Deactivate",Token.KEYWORD3);
            cKeywords.add("Escape",Token.KEYWORD3);
            cKeywords.add("Expose",Token.KEYWORD3);
            cKeywords.add("FocusIn",Token.KEYWORD3);
            cKeywords.add("FocusOut",Token.KEYWORD3);
            cKeywords.add("Gravity",Token.KEYWORD3);
            cKeywords.add("Key",Token.KEYWORD3);
            cKeywords.add("KeyPress",Token.KEYWORD3);
            cKeywords.add("KeyRelease",Token.KEYWORD3);
            cKeywords.add("Lock",Token.KEYWORD3);
            cKeywords.add("Meta",Token.KEYWORD3);
            cKeywords.add("Property",Token.KEYWORD3);
            cKeywords.add("Reparent",Token.KEYWORD3);
            cKeywords.add("Shift",Token.KEYWORD3);
            cKeywords.add("Unmap",Token.KEYWORD3);
            cKeywords.add("Visibility",Token.KEYWORD3);
            cKeywords.add("Button",Token.KEYWORD3);
            cKeywords.add("ButtonPress",Token.KEYWORD3);
            cKeywords.add("ButtonRelease",Token.KEYWORD3);
            cKeywords.add("Destroy",Token.KEYWORD3);
            cKeywords.add("Escape",Token.KEYWORD3);
            cKeywords.add("Enter",Token.KEYWORD3);
            cKeywords.add("Leave",Token.KEYWORD3);
            cKeywords.add("Motion",Token.KEYWORD3);
            cKeywords.add("MenuSelect",Token.KEYWORD3);
            cKeywords.add("Triple",Token.KEYWORD3);
            cKeywords.add("all",Token.KEYWORD3);
		}
		return cKeywords;
	}

	
	private static KeywordMap cKeywords;

	private boolean cpp;
	private KeywordMap keywords;
	private int lastOffset;
	private int lastKeyword;

	private boolean doKeyword(Segment line, int i, char c)
	{
		int i1 = i+1;

		int len = i - lastKeyword;
		byte id = keywords.lookup(line,lastKeyword,len);
		if(id != Token.NULL)
		{
			if(lastKeyword != lastOffset)
				addToken(lastKeyword - lastOffset,Token.NULL);
			addToken(len,id);
			lastOffset = i;
		}
		lastKeyword = i1;
		return false;
	}
}
