inst_map = [
	{"opcode": 0, "name": "OP_MOVE",  "body": 
		"setobjs2s(L, ra, RB(i));"},
	{"opcode": 1, "name": "OP_LOADK", "body": 
		"TValue *rb = k + GETARG_Bx(i);\n" 
		"setobj2s(L, ra, rb);"},
	{"opcode": 2, "name": "OP_LOADKX", "body": 
		"TValue *rb;\n"
		"lua_assert(GET_OPCODE(*ci->u.l.savedpc) == OP_EXTRAARG);\n"
		"rb = k + GETARG_Ax(*ci->u.l.savedpc++);\n"
		"setobj2s(L, ra, rb);"},
	{"opcode": 3, "name": "OP_LOADBOOL", "body": 
		"setbvalue(ra, GETARG_B(i));\n"
		"if (GETARG_C(i)) ci->u.l.savedpc++;  /* skip next instruction (if C) */"},
	{"opcode": 4, "name": "OP_LOADNIL", "body": 
		"int b = GETARG_B(i);\n"
		"do {\n"
		"	setnilvalue(ra++);\n"
		"} while (b--);"},
	{"opcode": 5, "name": "OP_GETUPVAL", "body":
		"int b = GETARG_B(i);\n"
		"setobj2s(L, ra, cl->upvals[b]->v);"},
	{"opcode": 6, "name": "OP_GETTABUP", "body":
		"int b = GETARG_B(i);\n"
	   "Protect(luaV_gettable(L, cl->upvals[b]->v, RKC(i), ra));"},
	{"opcode": 7, "name": "OP_GETTABLE", "body":
		"Protect(luaV_gettable(L, RB(i), RKC(i), ra));"},
	{"opcode": 8, "name": "OP_SETTABUP", "body":
		"int a = GETARG_A(i);\n"
		"Protect(luaV_settable(L, cl->upvals[a]->v, RKB(i), RKC(i)));"},
	{"opcode": 9, "name": "OP_SETUPVAL", "body":
		"UpVal *uv = cl->upvals[GETARG_B(i)];\n"
		"setobj(L, uv->v, ra);\n"
		"luaC_barrier(L, uv, ra);"},
	{"opcode": 10, "name": "OP_SETTABLE", "body":
		"Protect(luaV_settable(L, ra, RKB(i), RKC(i)));"},
	{"opcode": 11, "name": "OP_NEWTABLE", "body":
		"int b = GETARG_B(i);\n"
		"int c = GETARG_C(i);\n"
		"Table *t = luaH_new(L);\n"
		"sethvalue(L, ra, t);\n"
		"if (b != 0 || c != 0)\n"
		"	luaH_resize(L, t, luaO_fb2int(b), luaO_fb2int(c));\n"
		"checkGC(L, ra + 1);"},
	{"opcode": 12, "name": "OP_SELF", "body":
		"StkId rb = RB(i);\n"
		"setobjs2s(L, ra+1, rb);\n"
		"Protect(luaV_gettable(L, rb, RKC(i), ra));"},
	{"opcode": 13, "name": "OP_ADD", "body":
		"arith_op(luai_numadd, TM_ADD);"},
	{"opcode": 14, "name": "OP_SUB", "body":
		"arith_op(luai_numsub, TM_SUB);"},
	{"opcode": 15, "name": "OP_MUL", "body":
		"arith_op(luai_nummul, TM_MUL);"},
	{"opcode": 16, "name": "OP_DIV", "body":
		"arith_op(luai_numdiv, TM_DIV);"},
	{"opcode": 17, "name": "OP_MOD", "body":
		"arith_op(luai_nummod, TM_MOD);"},
	{"opcode": 18, "name": "OP_POW", "body":
		"arith_op(luai_numpow, TM_POW);"},
	{"opcode": 19, "name": "OP_UNM", "body":
		"TValue *rb = RB(i);\n"
		"if (ttisnumber(rb)) {\n"
		"	lua_Number nb = nvalue(rb);\n"
		"	setnvalue(ra, luai_numunm(L, nb));\n"
		"}\n"
		"else {\n"
		"	Protect(luaV_arith(L, ra, rb, rb, TM_UNM));\n"
		"}"},
	{"opcode": 20, "name": "OP_NOT", "body":
		"TValue *rb = RB(i);\n"
		"int res = l_isfalse(rb);  /* next assignment may change this value */\n"
		"setbvalue(ra, res);"},
	{"opcode": 21, "name": "OP_LEN", "body":
		"Protect(luaV_objlen(L, ra, RB(i)));"},
	{"opcode": 22, "name": "OP_CONCAT", "body":
		"int b = GETARG_B(i);\n"
		"int c = GETARG_C(i);\n"
		"StkId rb;\n"
		"L->top = base + c + 1;  /* mark the end of concat operands */\n"
		"Protect(luaV_concat(L, c - b + 1));\n"
		"ra = RA(i);  /* 'luav_concat' may invoke TMs and move the stack */\n"
		"rb = b + base;\n"
		"setobjs2s(L, ra, rb);\n"
		"checkGC(L, (ra >= rb ? ra + 1 : rb));\n"
		"L->top = ci->top;  /* restore top */"},
	{"opcode": 23, "name": "OP_JMP", "body":
		"dojump(ci, i, 0);"},
	{"opcode": 24, "name": "OP_EQ", "body":
		"TValue *rb = RKB(i);\n"
		"TValue *rc = RKC(i);\n"
		"Protect(\n"
		"if (cast_int(equalobj(L, rb, rc)) != GETARG_A(i))\n"
		"	ci->u.l.savedpc++;\n"
		"else\n"
		"	donextjump(ci);)"},
	{"opcode": 25, "name": "OP_LT", "body":
		"Protect(\n"
		"if (luaV_lessthan(L, RKB(i), RKC(i)) != GETARG_A(i))\n"
		"	ci->u.l.savedpc++;\n"
		"else\n"
		"	donextjump(ci);\n"
		")"},
	{"opcode": 26, "name": "OP_LE", "body":
		"Protect(\n"
		"if (luaV_lessequal(L, RKB(i), RKC(i)) != GETARG_A(i))\n"
		"	ci->u.l.savedpc++;\n"
		"else\n"
		"	donextjump(ci);\n"
		")"},
	{"opcode": 27, "name": "OP_TEST", "body":
		"if (GETARG_C(i) ? l_isfalse(ra) : !l_isfalse(ra))\n"
		"	ci->u.l.savedpc++;\n"
		"else\n"
		"	donextjump(ci);"},
	{"opcode": 28, "name": "OP_TESTSET", "body":
		"TValue *rb = RB(i);\n"
		"if (GETARG_C(i) ? l_isfalse(rb) : !l_isfalse(rb))\n"
		"	ci->u.l.savedpc++;\n"
		"else {\n"
		"	setobjs2s(L, ra, rb);\n"
		"	donextjump(ci);\n"
		"}"},
	{"opcode": 29, "name": "OP_CALL", "body":
		"int b = GETARG_B(i);\n"
		"int nresults = GETARG_C(i) - 1;\n"
		"if (b != 0) L->top = ra+b;  /* else previous instruction set top */\n"
		"if (luaD_precall(L, ra, nresults)) {  /* C function? */\n"
		"	if (nresults >= 0) L->top = ci->top;  /* adjust results */\n"
		"	base = ci->u.l.base;\n"
		"}\n"
		"else {  /* Lua function */\n"
		"	ci = L->ci;\n"
		"	ci->callstatus |= CIST_REENTRY;\n"
		"	goto newframe;  /* restart luaV_execute over new Lua function */\n"
		"}"},
	{"opcode": 30, "name": "OP_TAILCALL", "body":
		"int b = GETARG_B(i);\n"
		"if (b != 0) L->top = ra+b;  /* else previous instruction set top */\n"
		"lua_assert(GETARG_C(i) - 1 == LUA_MULTRET);\n"
		"if (luaD_precall(L, ra, LUA_MULTRET))  /* C function? */\n"
		"	base = ci->u.l.base;\n"
		"else {\n"
		"	/* tail call: put called frame (n) in place of caller one (o) */\n"
		"	CallInfo *nci = L->ci;  /* called frame */\n"
		"	CallInfo *oci = nci->previous;  /* caller frame */\n"
		"	StkId nfunc = nci->func;  /* called function */\n"
		"	StkId ofunc = oci->func;  /* caller function */\n"
		"	/* last stack slot filled by 'precall' */\n"
		"	StkId lim = nci->u.l.base + getproto(nfunc)->numparams;\n"
		"	int aux;\n"
		"	/* close all upvalues from previous call */\n"
		"	if (cl->p->sizep > 0) luaF_close(L, oci->u.l.base);\n"
		"	/* move new frame into old one */\n"
		"	for (aux = 0; nfunc + aux < lim; aux++)\n"
		"		setobjs2s(L, ofunc + aux, nfunc + aux);\n"
		"	oci->u.l.base = ofunc + (nci->u.l.base - nfunc);  /* correct base */\n"
		"	oci->top = L->top = ofunc + (L->top - nfunc);  /* correct top */\n"
		"	oci->u.l.savedpc = nci->u.l.savedpc;\n"
		"	oci->callstatus |= CIST_TAIL;  /* function was tail called */\n"
		"	ci = L->ci = oci;  /* remove new frame */\n"
		"	lua_assert(L->top == oci->u.l.base + getproto(ofunc)->maxstacksize);\n"
		"	goto newframe;  /* restart luaV_execute over new Lua function */\n"
		"}"},
	{"opcode": 31, "name": "OP_RETURN", "body":
		"int b = GETARG_B(i);\n"
		"if (b != 0) L->top = ra+b-1;\n"
		"if (cl->p->sizep > 0) luaF_close(L, base);\n"
		"b = luaD_poscall(L, ra);\n"
		"if (!(ci->callstatus & CIST_REENTRY))  /* 'ci' still the called one */\n"
		"	return;  /* external invocation: return */\n"
		"else {  /* invocation via reentry: continue execution */\n"
		"	ci = L->ci;\n"
		"	if (b) L->top = ci->top;\n"
		"	lua_assert(isLua(ci));\n"
		"	lua_assert(GET_OPCODE(*((ci)->u.l.savedpc - 1)) == OP_CALL);\n"
		"	goto newframe;  /* restart luaV_execute over new Lua function */\n"
		"}"},
	{"opcode": 32, "name": "OP_FORLOOP", "body":
		"lua_Number step = nvalue(ra+2);\n"
		"lua_Number idx = luai_numadd(L, nvalue(ra), step); /* increment index */\n"
		"lua_Number limit = nvalue(ra+1);\n"
		"if (luai_numlt(L, 0, step) ? luai_numle(L, idx, limit)\n"
		"		: luai_numle(L, limit, idx)) {\n"
		"	ci->u.l.savedpc += GETARG_sBx(i);  /* jump back */\n"
		"	setnvalue(ra, idx);  /* update internal index... */\n"
		"	setnvalue(ra+3, idx);  /* ...and external index */\n"
		"}"},
	{"opcode": 33, "name": "OP_FORPREP", "body":
		"const TValue *init = ra;\n"
		"const TValue *plimit = ra+1;\n"
		"const TValue *pstep = ra+2;\n"
		"if (!tonumber(init, ra))\n"
		"	luaG_runerror(L, LUA_QL(\"for\") \" initial value must be a number\");\n"
		"else if (!tonumber(plimit, ra+1))\n"
		"luaG_runerror(L, LUA_QL(\"for\") \" limit must be a number\");\n"
		"else if (!tonumber(pstep, ra+2))\n"
		"luaG_runerror(L, LUA_QL(\"for\") \" step must be a number\");\n"
		"setnvalue(ra, luai_numsub(L, nvalue(ra), nvalue(pstep)));\n"
		"ci->u.l.savedpc += GETARG_sBx(i);"},
	{"opcode": 34, "name": "OP_TFORCALL", "body":
		"StkId cb = ra + 3;  /* call base */\n"
		"setobjs2s(L, cb+2, ra+2);\n"
		"setobjs2s(L, cb+1, ra+1);\n"
		"setobjs2s(L, cb, ra);\n"
		"L->top = cb + 3;  /* func. + 2 args (state and index) */\n"
		"Protect(luaD_call(L, cb, GETARG_C(i), 1));\n"
		"L->top = ci->top;\n"
		"i = *(ci->u.l.savedpc++);  /* go to next instruction */\n"
		"ra = RA(i);\n"
		"lua_assert(GET_OPCODE(i) == OP_TFORLOOP);\n"
		"goto l_tforloop;"},
	{"opcode": 35, "name": "OP_TFORLOOP", "body":
		"l_tforloop:\n"
		"if (!ttisnil(ra + 1)) {  /* continue loop? */\n"
		"	setobjs2s(L, ra, ra + 1);  /* save control variable */\n"
		"	ci->u.l.savedpc += GETARG_sBx(i);  /* jump back */\n"
		"}"},
	{"opcode": 36, "name": "OP_SETLIST", "body":
		"{\n"
		"	int n = GETARG_B(i);\n"
		"	int c = GETARG_C(i);\n"
		"	int last;\n"
		"	Table *h;\n"
		"	if (n == 0) n = cast_int(L->top - ra) - 1;\n"
		"	if (c == 0) {\n"
		"		lua_assert(GET_OPCODE(*ci->u.l.savedpc) == OP_EXTRAARG);\n"
		"		c = GETARG_Ax(*ci->u.l.savedpc++);\n"
		"	}\n"
		"	luai_runtimecheck(L, ttistable(ra));\n"
		"	h = hvalue(ra);\n"
		"	last = ((c-1)*LFIELDS_PER_FLUSH) + n;\n"
		"	if (last > h->sizearray)  /* needs more space? */\n"
		"		luaH_resizearray(L, h, last);  /* pre-allocate it at once */\n"
		"	for (; n > 0; n--) {\n"
		"		TValue *val = ra+n;\n"
		"		luaH_setint(L, h, last--, val);\n"
		"		luaC_barrierback(L, obj2gco(h), val);\n"
		"	}\n"
		"	L->top = ci->top;  /* correct top (in case of previous open call) */\n"
		"}"},
	{"opcode": 37, "name": "OP_CLOSURE", "body":
		"Proto *p = cl->p->p[GETARG_Bx(i)];\n"
		"Closure *ncl = getcached(p, cl->upvals, base);  /* cached closure */\n"
		"if (ncl == NULL)  /* no match? */\n"
		"	pushclosure(L, p, cl->upvals, base, ra);  /* create a new one */\n"
		"else\n"
		"	setclLvalue(L, ra, ncl);  /* push cashed closure */\n"
		"checkGC(L, ra + 1);"},
	{"opcode": 38, "name": "OP_VARARG", "body":
		"int b = GETARG_B(i) - 1;\n"
		"int j;\n"
		"int n = cast_int(base - ci->func) - cl->p->numparams - 1;\n"
		"if (b < 0) {  /* B == 0? */\n"
		"	b = n;  /* get all var. arguments */\n"
		"	Protect(luaD_checkstack(L, n));\n"
		"	ra = RA(i);  /* previous call may change the stack */\n"
		"	L->top = ra + n;\n"
		"}\n"
		"for (j = 0; j < b; j++) {\n"
		"	if (j < n) {\n"
		"		setobjs2s(L, ra + j, base - n + j);\n"
		"	}\n"
		"	else {\n"
		"		setnilvalue(ra + j);\n"
		"	}\n"
		"}"},
	{"opcode": 39, "name": "OP_EXTRAARG", "body":
		"lua_assert(0);"}
]
