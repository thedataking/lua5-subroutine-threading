inst_map = [
	{"opcode": 0, "name": "OP_MOVE",  "body": 
		"setobjs2s(L, ra, RB(i));"},
	{"opcode": 1, "name": "OP_LOADK", "body": 
		"TValue *rb = k + GETARG_Bx(i);" 
		"setobj2s(L, ra, rb);"},
	{"opcode": 2, "name": "OP_LOADKX", "body": 
		"TValue *rb;"
		"lua_assert(GET_OPCODE(*ci->u.l.savedpc) == OP_EXTRAARG);"
		"rb = k + GETARG_Ax(*ci->u.l.savedpc++);"
		"setobj2s(L, ra, rb);"},
	{"opcode": 3, "name": "OP_LOADBOOL", "body": 
		"setbvalue(ra, GETARG_B(i));"
		"if (GETARG_C(i)) ci->u.l.savedpc++;  /* skip next instruction (if C) */"},
	{"opcode": 4, "name": "OP_LOADNIL", "body": 
		"int b = GETARG_B(i);"
		"do {"
		"	setnilvalue(ra++);"
		"} while (b--);"},
	{"opcode": 5, "name": "OP_GETUPVAL", "body":
		"int b = GETARG_B(i);"
		"setobj2s(L, ra, cl->upvals[b]->v);"},
	{"opcode": 6, "name": "OP_GETTABUP", "body":
		"int b = GETARG_B(i);"
	   "Protect(luaV_gettable(L, cl->upvals[b]->v, RKC(i), ra));"},
	{"opcode": 7, "name": "OP_GETTABLE", "body":
		"Protect(luaV_gettable(L, RB(i), RKC(i), ra));"},
	{"opcode": 8, "name": "OP_SETTABUP", "body":
		"int a = GETARG_A(i);"
		"Protect(luaV_settable(L, cl->upvals[a]->v, RKB(i), RKC(i)));"},
	{"opcode": 9, "name": "OP_SETUPVAL", "body":
		"UpVal *uv = cl->upvals[GETARG_B(i)];"
		"setobj(L, uv->v, ra);"
		"luaC_barrier(L, uv, ra);"},
	{"opcode": 10, "name": "OP_SETTABLE", "body":
		"Protect(luaV_settable(L, ra, RKB(i), RKC(i)));"},
	{"opcode": 11, "name": "OP_NEWTABLE", "body":
		"int b = GETARG_B(i);"
		"int c = GETARG_C(i);"
		"Table *t = luaH_new(L);"
		"sethvalue(L, ra, t);"
		"if (b != 0 || c != 0)"
		"	luaH_resize(L, t, luaO_fb2int(b), luaO_fb2int(c));"
		"checkGC(L, ra + 1);"},
	{"opcode": 12, "name": "OP_SELF", "body":
		"StkId rb = RB(i);"
		"setobjs2s(L, ra+1, rb);"
		"Protect(luaV_gettable(L, rb, RKC(i), ra));"},
	{"opcode": 13, "name": "OP_ADD", "body":
		"arith_op(luai_numadd, TM_ADD);"},
	{"opcode": 14, "name": "OP_SUB", "body":
		"arith_op(luai_numadd, TM_SUB);"},
	{"opcode": 15, "name": "OP_MUL", "body":
		"arith_op(luai_numadd, TM_MUL);"},
	{"opcode": 16, "name": "OP_DIV", "body":
		"arith_op(luai_numadd, TM_DIV);"},
	{"opcode": 17, "name": "OP_MOD", "body":
		"arith_op(luai_numadd, TM_MOD);"},
	{"opcode": 18, "name": "OP_POW", "body":
		"arith_op(luai_numadd, TM_POW);"},
	{"opcode": 19, "name": "OP_UNM", "body":
		"TValue *rb = RB(i);"
		"if (ttisnumber(rb)) {"
		"	lua_Number nb = nvalue(rb);"
		"	setnvalue(ra, luai_numunm(L, nb));"
		"}"
		"else {"
		"	Protect(luaV_arith(L, ra, rb, rb, TM_UNM));"
		"}"},
	{"opcode": 20, "name": "OP_NOT", "body":
		"TValue *rb = RB(i);"
		"int res = l_isfalse(rb);  /* next assignment may change this value */"
		"setbvalue(ra, res);"},
	{"opcode": 21, "name": "OP_LEN", "body":
		"Protect(luaV_objlen(L, ra, RB(i)));"},
	{"opcode": 22, "name": "OP_CONCAT", "body":
		"int b = GETARG_B(i);"
		"int c = GETARG_C(i);"
		"StkId rb;"
		"L->top = base + c + 1;  /* mark the end of concat operands */"
		"Protect(luaV_concat(L, c - b + 1));"
		"ra = RA(i);  /* 'luav_concat' may invoke TMs and move the stack */"
		"rb = b + base;"
		"setobjs2s(L, ra, rb);"
		"checkGC(L, (ra >= rb ? ra + 1 : rb));"
		"L->top = ci->top;  /* restore top */"},
	{"opcode": 23, "name": "OP_JMP", "body":
		"dojump(ci, i, 0);"},
	{"opcode": 24, "name": "OP_EQ", "body":
		"TValue *rb = RKB(i);"
		"TValue *rc = RKC(i);"
		"Protect("
		"if (cast_int(equalobj(L, rb, rc)) != GETARG_A(i))"
		"	ci->u.l.savedpc++;"
		"else"
		"	donextjump(ci);)"},
	{"opcode": 25, "name": "OP_LT", "body":
		"Protect("
		"if (luaV_lessthan(L, RKB(i), RKC(i)) != GETARG_A(i))"
		"	ci->u.l.savedpc++;"
		"else"
		"	donextjump(ci);"
		")"},
	{"opcode": 26, "name": "OP_LE", "body":
		"Protect("
		"if (luaV_lessequal(L, RKB(i), RKC(i)) != GETARG_A(i))"
		"	ci->u.l.savedpc++;"
		"else"
		"	donextjump(ci);"
		")"},
	{"opcode": 27, "name": "OP_TEST", "body":
		"if (GETARG_C(i) ? l_isfalse(ra) : !l_isfalse(ra))"
		"	ci->u.l.savedpc++;"
		"else"
		"	donextjump(ci);"},
	{"opcode": 28, "name": "OP_TESTSET", "body":
		"TValue *rb = RB(i);"
		"if (GETARG_C(i) ? l_isfalse(rb) : !l_isfalse(rb))"
		"	ci->u.l.savedpc++;"
		"else {"
		"	setobjs2s(L, ra, rb);"
		"	donextjump(ci);"
		"}"},
	{"opcode": 29, "name": "OP_CALL", "body":
		"int b = GETARG_B(i);"
		"int nresults = GETARG_C(i) - 1;"
		"if (b != 0) L->top = ra+b;  /* else previous instruction set top */"
		"if (luaD_precall(L, ra, nresults)) {  /* C function? */"
		"	if (nresults >= 0) L->top = ci->top;  /* adjust results */"
		"	base = ci->u.l.base;"
		"}"
		"else {  /* Lua function */"
		"	ci = L->ci;"
		"	ci->callstatus |= CIST_REENTRY;"
		"	goto newframe;  /* restart luaV_execute over new Lua function */"
		"}"},
	{"opcode": 30, "name": "OP_TAILCALL", "body":
		"int b = GETARG_B(i);"
		"if (b != 0) L->top = ra+b;  /* else previous instruction set top */"
		"lua_assert(GETARG_C(i) - 1 == LUA_MULTRET);"
		"if (luaD_precall(L, ra, LUA_MULTRET))  /* C function? */"
		"	base = ci->u.l.base;"
		"else {"
		"	/* tail call: put called frame (n) in place of caller one (o) */"
		"	CallInfo *nci = L->ci;  /* called frame */"
		"	CallInfo *oci = nci->previous;  /* caller frame */"
		"	StkId nfunc = nci->func;  /* called function */"
		"	StkId ofunc = oci->func;  /* caller function */"
		"	/* last stack slot filled by 'precall' */"
		"	StkId lim = nci->u.l.base + getproto(nfunc)->numparams;"
		"	int aux;"
		"	/* close all upvalues from previous call */"
		"	if (cl->p->sizep > 0) luaF_close(L, oci->u.l.base);"
		"	/* move new frame into old one */"
		"	for (aux = 0; nfunc + aux < lim; aux++)"
		"		setobjs2s(L, ofunc + aux, nfunc + aux);"
		"	oci->u.l.base = ofunc + (nci->u.l.base - nfunc);  /* correct base */"
		"	oci->top = L->top = ofunc + (L->top - nfunc);  /* correct top */"
		"	oci->u.l.savedpc = nci->u.l.savedpc;"
		"	oci->callstatus |= CIST_TAIL;  /* function was tail called */"
		"	ci = L->ci = oci;  /* remove new frame */"
		"	lua_assert(L->top == oci->u.l.base + getproto(ofunc)->maxstacksize);"
		"	goto newframe;  /* restart luaV_execute over new Lua function */"
		"}"},
	{"opcode": 31, "name": "OP_RETURN", "body":
		"int b = GETARG_B(i);"
		"if (b != 0) L->top = ra+b-1;"
		"if (cl->p->sizep > 0) luaF_close(L, base);"
		"b = luaD_poscall(L, ra);"
		"if (!(ci->callstatus & CIST_REENTRY))  /* 'ci' still the called one */"
		"	return;  /* external invocation: return */"
		"else {  /* invocation via reentry: continue execution */"
		"	ci = L->ci;"
		"	if (b) L->top = ci->top;"
		"	lua_assert(isLua(ci));"
		"	lua_assert(GET_OPCODE(*((ci)->u.l.savedpc - 1)) == OP_CALL);"
		"	goto newframe;  /* restart luaV_execute over new Lua function */"
		"}"},
	{"opcode": 32, "name": "OP_FORLOOP", "body":
		"lua_Number step = nvalue(ra+2);"
		"lua_Number idx = luai_numadd(L, nvalue(ra), step); /* increment index */"
		"lua_Number limit = nvalue(ra+1);"
		"if (luai_numlt(L, 0, step) ? luai_numle(L, idx, limit)"
		"		: luai_numle(L, limit, idx)) {"
		"	ci->u.l.savedpc += GETARG_sBx(i);  /* jump back */"
		"	setnvalue(ra, idx);  /* update internal index... */"
		"	setnvalue(ra+3, idx);  /* ...and external index */"
		"}"},
	{"opcode": 33, "name": "OP_FORPREP", "body":
		"const TValue *init = ra;"
		"const TValue *plimit = ra+1;"
		"const TValue *pstep = ra+2;"
		"if (!tonumber(init, ra))"
		"	luaG_runerror(L, LUA_QL("for") " initial value must be a number");"
		"else if (!tonumber(plimit, ra+1))"
		"luaG_runerror(L, LUA_QL("for") " limit must be a number");"
		"else if (!tonumber(pstep, ra+2))"
		"luaG_runerror(L, LUA_QL("for") " step must be a number");"
		"setnvalue(ra, luai_numsub(L, nvalue(ra), nvalue(pstep)));"
		"ci->u.l.savedpc += GETARG_sBx(i);"},
	{"opcode": 34, "name": "OP_TFORCALL", "body":
		"StkId cb = ra + 3;  /* call base */"
		"setobjs2s(L, cb+2, ra+2);"
		"setobjs2s(L, cb+1, ra+1);"
		"setobjs2s(L, cb, ra);"
		"L->top = cb + 3;  /* func. + 2 args (state and index) */"
		"Protect(luaD_call(L, cb, GETARG_C(i), 1));"
		"L->top = ci->top;"
		"i = *(ci->u.l.savedpc++);  /* go to next instruction */"
		"ra = RA(i);"
		"lua_assert(GET_OPCODE(i) == OP_TFORLOOP);"
		"goto l_tforloop;"},
	{"opcode": 35, "name": "OP_TFORLOOP", "body":
		},
	{"opcode": 36, "name": "OP_SETLIST", "body":
		},
	{"opcode": 37, "name": "OP_CLOSURE", "body":
		},
	{"opcode": 38, "name": "OP_VARARG", "body":
		},
	{"opcode": 39, "name": "OP_EXTRAARG", "body":
		}
]
