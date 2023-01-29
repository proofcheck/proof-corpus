# char_symbols = {"\\{": "{", "\\}": "}"}

term_operators = set(
    (
        # Table 50
        r"""
        \amalg \ast \bigcirc \bigtriangledown \bigtriangleup \bullet \cap \cdot \circ \cup \oslash \otimes \dagger
        \ddagger \diamond \div \lhd \mp \odot \ominus \oplus \oslash \otimes \pm \rhd \setminus \sqcap \sqcup \star
        \times \triangleleft \triangleright \unlhd \unrhd \uplus \vee \wedge \wr
        """
        # Table 51
        r"""
        \barwedge \boxdot \boxminus \boxplus \boxtimes \Cap \centerdot \circledast \circledcirc \circleddash \Cup
        \curlyvee \curlywedge \divideontimes \dotplus \doublebarwedge \intercal \leftthreetimes \ltimes \rightthreetimes
        \rtimes \smallsetminus \veebar
        """
        # Table 52
        r"""
        \baro \bbslash \binampersand \bindnasrepma \boxast \boxbar \boxbox \boxbslash \boxcircle \boxdot \boxempty
        \boxslash \curlyveedownarrow \curlyveeuparrow \curlywedgedownarrow \curlywedgeuparrow \fatbslash \fatsemi
        \fatslash \interleave \leftslice \merge \minuso \moo \nplus \obar \oblong \obslash \ogreaterthan \olessthan
        \ovee \owedge \rightslice \sslash \talloblong \varbigcirc \varcurlyvee \varcurlywedge \varoast \varobar
        \varobslash \varocircle \varodot \varogreaterthan \varolessthan \varominus \varoplus \varoslash \varotimes
        \varovee \varowedge \vartimes \Ydown \Yleft \Yright \Yup
        """
        # Table 53
        r"""
        \lhd \LHD \ocircle \rhd \RHD \unlhd \unrhd
        """
        # Table 54
        r"""
        \circledbar \circledbslash \circledvee \circledwedge \invamp \medbullet \medcirc \sqcapplus \sqcupplus
        """
        # Table 55
        r"""
        \ast \Asterisk \barwedge \bigstar \bigvarstar \blackdiamond \cap \circplus \coasterisk \coAsterisk \convolution
        \cup \curlyvee \curlywedge \divdot \divideontimes \dotdiv \dotplus \dottimes \doublebarwedge \doublecap
        \doublecup \ltimes \pluscirc \rtimes \sqbullet \sqcap \sqcup \sqdoublecap \sqdoublecup \square \squplus \udot
        \uplus \varstar \vee \veebar \veedoublebar \wedge
        """
        # Table 56
        r"""
        \amalg \ast \backslashdiv \bowtie \bullet \cap \capdot \capplus \cdot \circ \doublesqcup \doublevee \doublewedge
        \downtherefore \downY \dtimes \fivedots \hbipropto \hdotdot \lefthalfcap \righttherefore \rightthreetimes
        \rightY \rtimes \slashdiv \smallprod \sqcap \sqcapdot \sqcapplus \sqcup \closedcurlyvee \closedcurlywedge \cup
        \cupdot \cupplus \curlyvee \curlyveedot \curlywedge \curlywedgedot \ddotdot \diamonddots \div \dotmedvert
        \dotminus \doublecap \doublecup \doublecurlyvee \doublecurlywedge \doublesqcap \lefthalfcup \lefttherefore
        \leftthreetimes \leftY \times \medbackslash \medcircle \medslash \medvert \medvertdot \minus \minusdot \mp
        \neswbipropto \nwsebipropto \plus \pm \righthalfcap \righthalfcup \sqcupdot \sqcupplus \squaredots \times
        \udotdot \uptherefore \upY \utimes \vbipropto \vdotdot \vee \veedot \vertbowtie \vertdiv \wedge \wedgedot
        \wreath \setminuys \smallsetminus \Join \wr \shortmid \Cap \Cup \uplus
        """
        # Table 57
        r"""
        \amalg \ast \barwedge \bowtie \cap \capdot \capplus \cdot \centerdot \cup \cupdot \cupplus \curlyvee \curlywedge
        \ddotdot \div \divideontimes \divslash \dotminus \doublesqcup \doublevee \doublewedge \downY \dtimes \hdotdot
        \intercal \intprod \intprodr \leftthreetimes \leftY \ltimes \medbackslash \medslash \minus \minusdot \minusfdots
        \minusrdots \mp \rightY \rtimes \setminus \sqcap \sqcapdot \sqcapplus \sqcup \sqcupdot \sqcupplus \times
        \timesbar \udotdot \upbowtie \upY \utimes \varamalg \vdotdot \vdots \vee \dotplus \dottimes \doublebarwedge
        \doublecap \doublecup \doublesqcap \plus \plusdot \pm \pullback \pushout \rightthreetimes \veebar \veedot
        \veedoublebar \wedge \wedgedot \wreath \btimes \Cap \Cup \hookupminus \hourcglass \land \lor \minushookup
        \smalldivslash \smallsetminus \Sqcap \Sqcup \ttimes \lJoin \rJoin \Join \lrtimes \uplus \veeonvee \wedgeonwedge
        \wr
        """
        # Table 58
        r"""
        \ast \baro \barwedge \bbslash \binampersand \bindnasrepma \blackbowtie \bowtie \cap \Cap \cdot \centerdot
        \circplus \coAsterisk \convolution \cup \Cup \cupleftarrow \curlyvee \curlywedge \dagger \ddagger \div
        \divideontimes \dotplus \dottimes \doublebarwedge \fatsemi \gtrdot \intercal \lbag \lblackbowtie \leftslice
        \leftthreetimes \lessdot \times \ltimesblack \merge \minuso \moo \mp \nplus \pluscirc \plustrif \pm \rbag
        \rblackbowtie \rightslice \rightthreetimes \rtimes \rtimesblack \smallsetminus \smashtimes \squplus \sslash
        \times \uplus \varcap \varcup \varintercal \varsqcap \varsqcup \vartimes \vee \Vee \veebar \veeonvee \wedge
        \Wedge \Ydown \Yleft \Yright \Yup
        """
        r"""
        \amalg \ast \barcap \barcup \barvee \barwedge \bigslopedvee \bigslopedwedge \btimes \cap \Cap \capbarcup \capdot
        \capovercup \capwedge \closedvarcap \closedvarcup \closedvarcupsmashprod \commaminus \cup \Cup \cupbarcap
        \cupdot \cupleftarrow \cupovercap \cupvee \curlyvee \curlywedge \dagger \ddagger \div \divideontimes \dotminus
        \dotplus \dottimes \doublebarvee \doublebarwedge \doubleplus \dsol \eggplus \fcmp \fracslash \intercal
        \interleave \intprod \intprodr \invlazys \leftthreetimes \lhd \ltimes \midbarvee \midbarwedge \minusdot
        \minusfdots \minusrdots \mp \nhVvert \opluslhrim \oplusrhrim \otimeslhrim \otimesrhrim \plusdot \pluseqq
        \plushat \plussim \plussubtwo \plustrif \pm \rhd \rightthreetimes \ringplus \rsolbar \rtimes \setminus \shuffle
        \simplus \smallsetminus \smashtimes \sqcap \Sqcap \sqcup \Sqcup \sslash \threedotcolon \times \timesbar \tminus
        \tplus \tripleplus \trslash \twocaps \twocups \typecolon \uminus \unlhd \unrhd \upand \uplus \varbarwedge
        \vardoublebarwedge \varveebar \vectimes \Vee \vee \veebar \veedot \veedoublebar \veemidvert \veeodot \veeonvee
        \Wedge \wedge \wedgebar \wedgedot \wedgedoublebar \wedgemidvert \wedgeodot \wedgeonwedge \wr \land \lor
        \doublecap \doublecup
        """
        # Table 60
        r"""\dtimes \udtimes \utimes"""
        # Table 61
        r"""\parr \with"""
        # Table 62
        r"""\cshuffle \shuffle"""
        # Table 63
        r"""\odplus"""
        # Table 64
        r"""
        \blacktriangledown \blacktriangleleft \blacktriangleright \blacktriangleup \boxasterisk \boxbackslash \boxbot
        \boxcirc \boxcoasterisk \boxdiv \boxdot \boxleft \boxminus \boxplus \boxright \boxslash \boxtimes \boxtop
        \boxtriangleup \boxvoid \oasterisk \backslash \obot \ocirc \ocoasterisk \odiv \odot \oleft \ominus \oplus
        \oright \oslash \otimes \otop
        """
        # Table 65
        r"""
        \boxbackslash \boxbox \boxdot \boxminus \boxplus \boxslash \boxtimes \boxvert \diamondbackslash \diamonddiamond
        \diamonddot \diamondminus \diamondplus \diamondslash \diamondtimes \diamondvert \downslice \filleddiamond
        \filledmedsquare \filledmedtriangledown \filledmedtriangleleft \filledmedtriangleright \filledmedtriangleup
        \filledsquare \filledstar \filledtriangledown \filledtriangleleft \filledtriangleright \filledtriangleup
        \meddiamond \medsquare \medstar \medtriangledown \medtriangleleft \medtriangleright \medtriangleup \oast
        \obackslash \ocirc \odot \ominus \oplus \oslash \ostar \otimes \otriangle \overt \pentagram \smalldiamond
        \smallsquare \smallstar \smalltriangledown \smalltriangleleft \smalltriangleright \smalltriangleup \thinstar
        \upslice \blackquare \square \Box \Diamond \star \circledast \circledcirc \circleddash
        """
        # Table 66
        r"""
        \boxbackslash \boxbox \boxdot \boxminus \boxplus \boxslash \boxtimes \boxvert \diamondbackslash \diamonddiamond
        \diamonddot \diamondminus \diamondplus \diamondslash \diamondtimes \diamondvert \medblackcircle \medblackdiamond
        \medblacksquare \medblackstar \medblacktriangledown \medblacktriangleleft \medblacktriangleright
        \medblacktriangleup \medcircle \meddiamond \medslash \medsquare \medtriangledown \medtriangleleft
        \medtriangleright \medtriangleup \medwhitestar \oast \obackslash \ocirc \odash \odot \oequal \ominus \oplus
        \oslash \otimes \overt \smallblackcircle \smallblackdiamond \smallblacksquare \\smallblackstar
        \smallblacktriangledown \smallblacktriangleleft \smallblacktriangleright \smallblacktriangleup \smallcircle
        \smalldiamond \smallsquare \smalltriangledown \smalltriangleleft \smalltriangleright \smalltriangleup
        \smallwhitestar \blackdiamond \blacktriangle \blacktriangledown \blacktriangleleft \blacktriangleright \Box
        \boxbar \boxbslash \boxdiag \bullet \circ \circledast \circledcirc \circleddash \circledequal \circledvert
        \diamond \Diamond \diamondbslash \diamondcdot \mdblkdiamond \mdblksquare \mdlgblkcircle \mdlgblkdiamond
        \mdlgblksquare \mdlgwhtcircle \mdlgwhtdiamond \ndlgwhtsquare \mdwhtdiamond \mdwhtsquare \medstar \obslash
        \smblkcircle \smblkdiamond \smblksquare \smwhitestar \smwhtcircle \smwhtdiamond \smwhtsquare \square \star
        \triangle \triangledown \triangleleft \triangleright \vartriangle
        """
        # Table 67
        r"""
        \blacklozenge \blacksquare \blacktriangle \blacktriangledown \blacktriangleleft \blacktriangleright \boxast
        \boxbar \boxbot \boxbox \boxbslash \boxcircle \boxdivision \boxdot \boxleft \boxminus \boxplus \boxright
        \boxslash \boxtimes \boxtop \boxtriangle \circledast \circledcirc \circleddash \diamond \diamondbar
        \diamondcircle \diamondminus \diamondop \diamondplus \diamondtimes \diamondtriangle \obar \oblong \obot \obslash
        \ogreaterthan \oleft \olessthan \ominus \oplus \oright \oslash \otimes \otop \otriangle \ovee \owedge \star
        \talloblong
        """
        # Table 68
        r"""
        \blackhourglass \boxast \boxbar \boxbox \boxbslash \boxcircle \boxdiag \boxdot \boxminus \boxplus \boxtimes
        \circledast \circledcirc \circleddash \circledequal \circledparallel \circledvert \circlehbar \concavediamond
        \concavediamondtickleft \concavediamondtickright \diamond \dsub \hourglass \lozengeminus \mdlgblklozenge
        \mdlgwhtcircle \obar \obot \obslash \odiv \odot \odotslashdot \ogreaterthan \olcross \olessthan \ominus \operp
        \oplus \oslash \otimes \Otimes \otimeshat \rsub \smblkcircle \star \talloblong \triangle \triangleminus
        \triangleplus \triangleserifs \triangletimes \vysmblkcircle \vysmwhtcircle \whitesquaretickleft
        \whitesquaretickright \bullet
        """
        # Table 70
        r"""
        \smallawint \smallcirfnint \smallfint \smalliiiint \smalliiint \smalliint \smallint \smallintbar \smallintBar
        \smallintcap \smallintclockwise \smallintcup \smallintlarhk \smallintx \smalllowint \smallnpolint \smalloiiint
        \smalloiint \smalloint \smallointctrclockwise \smallpointint \smallrppolint \smallscpolint \smallsqint
        \smallsumint \smallupint \smallvarointclockwise
        """
        # Table 71
        r"""
        \smallawintsl \smallcirfnintsl \smallfintsl \smalliiiintsl \smalliiintsl \smalliintsl \smallintbarsl
        \smallintBarsl \smallintcapsl \smallintclockwisesl \smallintcupsl \smallintlarhksl \smallintsl \smallintxsl
        \smalllowintsl \smallnpolintsl \smalloiiintsl \smalloiintsl \smallointctrclockwisesl \smallointsl
        \smallpointintsl \smallrppolintsl \smallscpolintsl \smallsqintsl \smallsumintsl \smallupintsl
        \smallvarointclockwisesl \smallawintup \smallcirfnintup \smallfintup \smalliiiintup \smalliiintup \smalliintup
        \smallintBarup \smallintbarup \smallintcapup \smallintclockwiseup \smallintcupup \smallintlarhkup \smallintup
        \smallintxup \smalllowintup \smallnpolintup \smalloiiintup \smalloiintup \smallointctrclockwiseup \smallointup
        \smallpointintup \smallrppolintup \smallscpolintup \smallsqintup \smallsumintup \smallupintup
        \smallvarointclockwiseup
        """
        # Table 72
        r"""
        \bigcap \bigcup \bigodot \bigoplus \bigotimes \bigsqcup \biguplus \bigvee \bigwedge \coprod \int \oint \prod
        \sum
        """
        # Table 73
        r"""
        \iint \iiiint \iiint \idotsint
        """
        # Table 74
        r"""
        \bigbox \bigcurlyvee \bigcurlywedge \biginterleave \bignplus \bigparallel \bigsqcap \bigtriangledown
        \bigtriangleup
        """
        # Table 75
        r"""
        \int \oint \iint \oiint \iiint \varint \varoint
        """
        # Table 76
        r"""
        \bigcurlyvee \bigsqcap \bigcurlywedge \bigboxasterisk \bigboxbackslash \bigboxbot \bigboxcirc \bigboxcoasterisk
        \bigboxdiv \bigboxdot \bigboxleft \bigboxminus \bigboxplus \bigboxright \bigboxslash \bigboxtimes \bigboxtop
        \bigboxtriangleup \bigboxvoid \bigcomplementop \bigoasterisk \bigobackslash \bigobot \bigocirc \bigocoasterisk
        \bigodiv \bigoleft \bigominus \bigoright \bigoslash \bigotop \bigotriangleup \bigovoid \bigplus \bigsquplus
        \bigtimes \iiint \iint \int \oiint \oint
        """
        # Table 77
        r"""
        \bigsqcapplus \bigsqcupplus \fint \idotsint \iiiint \iiint \iint \oiiintclockwise \oiiintctrclockwise \oiiint
        \oiintclockwise \oiintctrclockwise \oiint \ointclockwise \ointctrclockwise \sqiiint \sqiint \sqint
        \varoiiintclockwise \varoiiintctrclockwise \varoiintclockwise \varoiintctrclockwise \varointclockwise
        \varointctrclockwise \varprod
        """
        # Table 78
        r"""
        \dotsint \fint \iiiint \iiint \iint \landdownint \landupint \oiint \ointclockwise \ointctrclockwise \sqiint
        \sqint \varoiint \varointclockwise \varointctrclockwise
        """
        # Table 79
        r"""
        \bigint \bigints \bigintss \bigintsss \bigintssss \bigoint \bigoints \bigointss \bigointsss \bigointssss
        """
        # Table 80
        r"""
        \bigcap \bigcapdot \bigcapplus \bigcircle \bigcup \bigcupdot \bigcupplus \bigcurlyvee \bigcurlyveedot
        \bigcurlywedge \bigcurlywedgedot \bigdoublecurlyvee \bigdoublecurlywedge \bigdoublevee \bigdoublewedge \bigoast
        \bigobackslash \bigocirc \bigodot \bigominus \bigoplus \bigoslash \bigostar \bigotimes \bigotriangle \bigovert
        \bigplus \bigsqcap \bigsqcapdot \bigsqcapplus \bigsqcup \bigsqcupdot \bigsqcupplus \bigtimes \bigvee \bigveedot
        \bigwedge \bigwedgedot \complement \coprod \idotsint \iiiint \iiint \iint \int \landdownint \landupint
        \circleleftint \lcirclerightint \oiint \oint \prod \rcircleleftint \rcirclerightint \strokedint \sum \sumint
        """
        # Table 81
        r"""
        \bigcap \bigcapdot \bigsqcup \bigqcupdot \landupint \lcircleleftint \bigcapplus \bigcup \bigcupdot \bigcupplus
        \bigcurlyvee \bigcurlywedge \bigdoublevee \bigdoublewedge \bigoast \bigodot \bigoplus \bigotimes \bigplus
        \bigsqcap \bigsqcapdot \bigsqcapplus \bigsqcupplus \bigtimes \bigvee \bigveedot \bigwedge \bigwedgedot \coprod
        \fint \idotsint \iiiint \iiint \iint \int \intbar \intBar \landdownint \lcirclerightint \oiiint \oiint \oint
        \osum \prod \rcircleleftint \rcirclerightint \sum \sumint \varcoprod \varosum \varprod \varsum \varsumint \awint
        \biguplus \conjquant \disquant \dotsint \intclockwise \intctrclockwise \modtwosum \ointclockwise
        \ointctrclockwise \varmodtwosum \varointclockwise \varointctrclockwise
        """
        # Table 82
        r"""
        \intup
        """
        # Table 83
        r"""
        \awint \Bbbsum \bigcap \bigcup \bigcupdot \bigodot \bigoplus \bigotimes \bigsqcap \bigsqcup \bigtalloblong
        \bigtimes \biguplus \bigvee \bigwedge \cirfnint \conjquant \coprod \disjquant \fint \iiiint \iiint \iint \int
        \intbar \intBar \intcap \intclockwise \intcup \intlarhk \intx \lowint \modtwosum \npolint \oiiint \oiint \oint
        \ointctrclockwise \pointint \prod \rppolint \scpolint \sqint \sum \sumint \upint \varointclockwise \xbsol \xsol
        """
        # Table 84
        r"""
        \intsl \iintsl \iiintsl \ointsl \oiintsl \oiiintsl \intclockwisesl \varointclockwisesl \ointctrclockwisesl
        \sumintsl \iiiintsl \intbarsl \intBarsl \fintsl \cirfnintsl \awintsl \rppolintsl \scpolintsl \npolintsl \intup
        \iintup \iiintup \ointup \oiintup \oiiintup \intclockwiseup \varointclockwiseup \ointctrclockwiseup \sumintup
        \iiiintup \intbarup \intBarup \fintup \cirfnintup \awintup \rppolintup \scpolintup \npolintup \pointintsl
        \sqintsl \intlarhksl \intxsl \intcapsl \intcupsl \upintsl \lowintsl \pointintup \sqintup \intlarhkup \intxup
        \intcapup \intcupup \upintup \lowintup
        """
        # Table 85
        r"""
        \awint \barint \cirfnint \doublebarint \downint \fint \npolint \oiiint \oiint \oint \ointclockwise
        \ointctrclockwise \idotsint \iiiint \iiint \iint \int \intcap \intclockwise \intcup \intlarhk \landdownint
        \landupint \pointint \rppolint \scpolint \sqiint \sqint \sumint \upint \varidotsint \varointclockwise
        \varointctrclockwise \xint \longint \longiint \longoint \longoiint
        """
        # Table 86
        r"""
        \intclockwise \oiiint \oiint \ointclockwise \ointctrclockwise"
        """
        # Table 87
        r"""
        \prodi \Prodi \PRODI
        """
        # Table 88
        r"""
        \bigparr \bigwith
        """
        # Table 183
        r"""
        \arccos \arcsin \arctan \arg \cos \cosh \cot \coth \csc \deg \det \dim \exp \gcd \hom \inf \ker \lg \lim \liminf
        \limsup \ln \log \max \min \Pr \sec \sin \sinh \sup \tan \tanh
        """
        # Table 184
        r"""
        \injlim \varinjlim \projlim \varliminf \varlimsup \varprojlim
        """
        # Table 185
        r"""
        \adj \arccot \arcosh \arcoth \arcsch \arsech \arsinh \artanh \Aut
        \Conv \Cov \cov \csch \curl \divg \End \erf \grad
        \id \Id \im \Im \lb \lcm \rank \Re \rot
        \sech \sgn \spa \tr \Var \Zu
        """
        # Table 186
        r"""
        \bigo \bigO \lito
        """
        # Table 203 (split)
        r"""
        \partial \Re \Im \wp
        """
        # Table 204 (split)
        r"""
        \complement
        """
        # Table 206 (split)
        r"""
        \complement \Finv \Game \partial \partialslash
        """
        # Table 207 (split)
        r"""
        \powerset \wp
        """
        # Table 208 (split)
        r"""
        \complement \Finv \Game \wp
        """
        # Table 209 (split)
        r"""
        \complement \Finv \Game \wp
        """
        # Table 214
        r"""
        \partial \varpartialdiff
        """
        # Table 227 (split)
        r"""
        \divides
        """
        # Table 246 (partial)
        r"""
        \sqrt
        """
        # Table 252 (partial)
        r"""
        \longdivision \sqrt
        """
        # Table 260
        r"""
        \sqrt*
        """
        # Table 302 (split)
        r"""
        \surd \nabla \angle
        """
    ).split()
)

formula_operators = set(
    (
        # Table 89
        r"""
        \approx \asymp \bowtie \cong \dashv \doteq \equiv \frown \Join \midt \models \parallel \perp \prec \preceq
        \propto \sim \simeq \smile \succ \succeq \vdash
        """
        # Table 90
        r"""
        \approxeq \backepsilon \backsim \backsimeq \because \between \Bumpeq \bumpeq \circeq \curlyeqprec \curlyegsucc
        \doteqdot \eqcirc \fallingdotseq \multimap \pitchfork \precapprox \preccurlyeq \precsim \risingdotseq \shortmid
        \shortparallel \smallfrown \smallsmile \succapprox \succcurlyeq \succsim \therefore \thickapprox \thicksim
        \varpropto \Vdash \vDash \Vvdash
        """
        # Table 91
        r"""
        \ncong \nmid \nparallel \nprec \npreceq \nshortmid \nshortparallel \nsim \nsucc \nsucceq \nvDash \nvdash \nVDash
        \precnapprox \precnsim \succnapprox \succnsim
        """
        # Table 92
        r"""
        \inplus \niplus
        """
        # Table 93
        r"""
        \invneg \Join \leadsto \logof \wasypropto
        """
        # Table 94
        r"""
        \circledgtr \circledless \colonapprox \Colonapprox \coloneq \Coloneq \Coloneqq \coloneqq \Colonsim \colonsim
        \Eqcolon \eqcolon \eqqcolon \Eqqcolon \eqsim \lJoin \Irtimes \multimap \multimapboth \multimapbothvert
        \multimapdot \multimapdotboth \multimapdotbothA \multimapdotbothAvert \multimapdotbothB \multimapdotbothBvert
        \multimapdotbothvert \multimapdotinv \multimapinv \openJoin \opentimes \Perp \preceqq \precneqq \rJoin
        \strictfi \strictif \strictiff \succeqq \succneqq \varparallel \varparallelinv \VvDash
        """
        # Table 95
        r"""
        \napproxeq \nasymp \nbacksim \nbacksimeq \nbumpeq \nBumpeq \nequiv \nprecapprox \npreccurlyeq \npreceqq
        \nprecsim \nsimeq \nsuccapprox \nsucccurlyeq \nsucceqq \nsuccsim \nthickapprox \ntwoheadleftarrow
        \ntwoheadrightarrow \nvarparallel \nvarparallelinv \nVdash
        """
        # Table 96
        r"""
        \between
        \botdoteq \Bumpedeq \bumpedeq \circeq \coloneq \corresponds \curlyeqprec \curlyeqsucc \DashV \Dashv \dashVv
        \divides \dotseq \eqbumped \eqcirc \eqcolon \fallingdotseq \ggcurly \llcurly \precapprox \preccurlyeq \precdot
        \precsim \risingdotseq \succapprox \succcurlyeq \succdot \succsim \therefore \topdoteq \vDash \Vdash \VDash
        \Vvdash
        """
        # Table 97
        r"""
        \napprox \ncong \ncurlyeqprec \ncurlyeqsucc \nDashv \ndashV \ndashv \nDashV \ndashVv \neq \notasymp \notdivides
        \notequiv \notperp \nprec \nprecapprox \npreccurlyeq \npreceq \nprecsim \nsim \nsimeq \nsucc \nsuccapprox
        \nsucccurlyeq \nsucceq \nsuccsim \nvDash \nVDash \nVdash \nvdash \nVvash \precnapprox \precneq \precnsim
        \succnapprox \succneq \succnsim
        """
        # Table 98
        r"""
        \approx \approxeq \backapprox \backapproxeq \backcong \backeqsim \backsim \backsimeq \backtriplesim \between
        \bumpeq \hateq \crossing \leftfootline \leftfree \leftmodels \leftModels \leftpropto \leftrightline
        \Leftrightline \leftslice \leftVdash \rightpropto \rightslice \rightVdash \rightvdash \risingdotseq \sefootline
        \sefree \seModels \semodels \separated \seVdash\Bumpeq \circeq \closedequal \closedprec \closedsucc \coloneq
        \cong \curlyeqprec \curlyeqsucc \Doteq \doteq \downfootline \downfree \downmodels \downModels \downpropto
        \downvdash \downVdash \eqbump \eqcirc \eqdot \eqsim \equal \equalclosed \equiv \equivclosed \fallingdotseq
        \leftvdash \nefootline \nefree \neModels \nemodels \neswline \Neswline \neVdash \nevdash \nwfootline \nwfree
        \nwmodels \nwModels \nwsecrossing \wseline \nwseline \nwvdash \nwVdash \prec \precapprox \preccurlyeq \preceq
        \precsim \rightfootline \rightfree \rightmodels \rightModels \sevdash \shortparallel \sim \simeq \succ
        \succapprox \succcurlyeq \succeq \succsim \swfootline \swfree \swModels \swmodels \swVdash \swvdash \triplesim
        \updownline \Updownline \upfootline \upfree \upModels \upmodels \uppropto \upvdash \upVdash \vcrossing \Vvdash
        \dashv \diagdown \diagup \divides \doteqdot \models \parallel \perp \propto \relbar \Relbar \varpropto \vDash
        \VDash \vdash \Vdash
        """
        # Table 99
        r"""
        \napprox \napproxeq \nbackapprox \nbackapproxeq \nbackcong \nbackegsim \nbacksim \nbacksimeq \nbacktriplesim
        \nbumpeq \nBumpeq \ncirceq \nclosedequal \ncong \ncurlyeqprec \ncurlyeqsucc \ndoteq \nDoteq \ndownfootline
        \ndownfree \ndownModels \ndownmodels \ndownVdash \ndownvdash \neqbump \neqcirc \neqdot \neqsim \nequal
        \nequalclosed \nequiv \nequivclosed \neswcrossing \nfallingdotseq \nhateq \nleftfootline \nleftfree \nleftmodels
        \nleftModels \nleftrightline \nLeftrightline \nleftvdash \nleftVdash \nnefootline \nnefree \nnemodels \nneModels
        \nneswline \nNeswline \nneVdash \nnevdash \nnwfootline \nnwfree \nnwmodels \nnwModels \nNwseline \nnwseline
        \nnwvdash \nnwVdash \nprec \nprecapprox \npreccurlyeq \npreceq \nprecsim \rightfootline \nrightfree \rightModels
        \nrightmodels \nrightvdash \nrightVdash \nrisingdotseq \nsefootline \nsefree \nseModels \nsemodels \nsevdash
        \nseVdash \nshortmid \nshortparallel \nsim \nsimeq \nsucc \nsuccapprox \nsucccurlyeq \nsucceq \nsuccsim
        \nswfootline \nswfree \nswModels \nswmodels \nswvdash \nswVdash \ntriplesim \nUpdownline \nupdownline
        \nupfootline \nupfree \nupModels \nupmodels \nupVdash \nupvdash \precnapprox \precnsim \succnapprox \succnsim
        \ndashv \ndiagdown \ndiagup \ndivides \ne \neq \nmid \nmodels \nparallel \nperp \nrelbar \nRelbar \nvDash
        \nvdash \nVdash \nVDash
        """
        # Table 100
        r"""
        \approx \approxeq \backcong \backpropto \backsim \backsimeg \between \bowtie \bumpeq \Bumpeq \bumpeqq \circeq
        \coloneq \cong \crossing \curlyeqprec \curlyeqsucc \dashVv \Ddashv \dotcong \doteq \Doteq \dotsminusdots
        \downAssert \downassert \downmodels \downvDash \downVdash \downvdash \downVDash \eqcirc \eqcolon \eqdot \eqsim
        \equal \equiv \fallingdotseq \frown \frowneq \frownsmile \in \leftassert \leftAssert \leftfootline \leftmodels
        \leftvdash \leftvDash \leftVdash \leftVDash \longleftfootline \Longmapsfrom \longmapsfrom \longrightfootline
        \mid \owns \parallel \prec \precapprox \preccurlyeq \preceq \preceqq \precnapprox \precneq \precneqq \precnsim
        \precsim \propto \rightassert \rightAssert \rightfootline \rightmodels \rightVdash \rightVDash \rightvdash
        \rightvDash \risingdotseq \shortmid \shortparallel \sim \simeq \smile \smileeq \smilefrown \stareq \succ
        \succapprox \succcurlyeq \succeq \succeqq \succsim \thickapprox \thicksim \triplesim \upassert \upAssert
        \upmodels \upvdash \upvDash \upVdash \upVDash \vDdash \veeeq \Vvdash \wedgeq \approxident \arceq \Assert \assert
        \asymp \Barv \barV \closure \coloneqq \dashv \DashV \Dashv \dashV \doteqdot \eqqcolon \hateq \Join \longdashv
        \models \ni \perp \propfrom \shortdowntack \shortlefttack \shortrighttack \shortuptack \smallfrown \smallsmile
        \varpropto \vBar \Vbar \vDash \VDash \Vdash \vdash \vlongdash
        """
        # Table 101
        r"""
        \backsimneqq \napprox \napproxeq \nbackcong \nbacksim \nbacksimeq \nbumpeq \nBumpeq \nbumpeqq \ncirceq \ncong
        \ncurlyeqprec \ncurlyeqsucc \ndashVv \nDdashv \ndoteq \nDoteq \ndownassert \ndownAssert \ndownmodels \ndownvdash
        \ndownVdash \ndownVDash \ndownvDash \neqcirc \neqdot \neqsim \nequal \nequiv \nfallingdotseq \nfrown \nfrowneq
        \nfrownsmile \nin \nleftAssert \nleftassert \nleftfootline \nleftmodels \nleftvDash \nleftvdash \nleftVdash
        \nleftVDash \nlongleftfootline \nLongmapsfrom \nlongmapsfrom \nlongrightfootline \nmid \nowns \nparallel \nprec
        \nprecapprox \npreccurlyeq \npreceq \npreceqq \nprecsim \nrightassert \rightAssert \nrightfootline \nrightmodels
        \nrightvdash \nrightVdash \nrightvDash \nrightVDash \nrisingdotseq \nshortmid \nshortparallel \nsim \nsimeq
        \nsmile \nsmileeq \nsmilefrown \nstareq \nsucc \nsuccapprox \nsucccurlyeq \nsucceq \nsucceqq \nsuccsim
        \ntriplesim \nupassert \nupAssert \nupmodels \nupVDash \nupvDash \nupVdash \nupvdash \nvDdash \nveeeq \nVvdash
        \nwedgeq \precneq \precneqq \simneqq \succnapprox \succneq \succneqq \succnsim \napproxident \narceq \nAssert
        \nassert \nasymp \nBarv \nbarV \nclosure \nDashV \nDashv \ndashv \ndashV \ne \neq \nhateq \nlongdashv \nmodels
        \nni \notin \nperp \nshortdowntack \nshortlefttack \nshortrighttack \nshortuptack \nsime \nvBar \nVbar \nVdash
        \nvDash \nVDash \nvdash \nvlongdash
        """
        # Table 102
        r"""
        \ac \approxeq \arceq \backsim \backsimeq \bagmember \because \between \bumpeq \Bumpeq \circeq \CircledEq \cong
        \corresponds \curlyeqprec \curlyeqsucc \dashV \DashV \dashVv \dfourier \Dfourier \disin \doteq \doteqdot
        \dotminus \dotsim \eqbumped \eqcirc \eqsim \equalparallel \fallingdotseq \fatbslash \fatslash \fork \frown
        \ggcurly \hash \inplus \kernelcontraction \llcurly \multimap \multimapboth \multimapbothvert \multimapdot
        \multimapdotboth \multimapdotbothA \multimapdotbothAvert \multimapdotbothB \multimapdotbothBvert
        \multimapdotbothvert \multimapdotinv \multimapinv \niplus \nisd \Perp \pitchfork \precapprox \preccurlyeq
        \precnapprox \precneqq \precnsim \precsim \prurel \risingdotseq \scurel \shortmid \shortparallel \simrdots
        \smallfrown \smallsmile \smile \strictfi \strictif \succapprox \succcurlyeq \succnapprox \succneqq \succnsim
        \succsim \therefore \thickapprox \thicksim \topfork \triangleq \varhash \varisins \varnis \varpropto \Vdash
        \vDash \VDash \veeeq \Vvdash \ztransf \Ztransf
        """
        # Table 103
        r"""
        \ncong \neq \nequiv \nmid \nparallel \nprec \npreceq \nshortmid \nshortparallel \nsim \nsucc \nsucceq \nVDash
        \nVdash \nvdash \nvDash
        """
        # Table 104
        r"""
        \approx \approxeq \approxeqq \approxident \arceq \assert \asteq \asymp \backcong \backsim \backsimeq \bagmember
        \Barv \barV \between \bNot \bowtie \Bumpeq \bumpeq \bumpeqq \cirbot \circeq \cirmid \closure \Coloneq \coloneq
        \cong \congdot \curlyeqprec \curlyeqsucc \dashcolon \dashv \dashV \Dashv \DashV \DashVDash \dashVdash \ddotseq
        \disin \Doteq \doteq \dotequiv \dotsim \dotsminusdots \downfishtail \dualmap \eparsl \eqcirc \eqcolon \eqdef
        \eqdot \eqvparsl \fallingdotseq \fbowtie \forksnot \forkv \frown \gleichstark \hatapprox \imageof \in \isindot
        \isinE \isinobar \isins \isinvb \kernelcontraction \leftdbltail \leftfishtail \lefttail \lfbowtie \lftimes
        \longdashv \lsqhook \measeq \mid \midcir \mlcp \models \multimap \multimapinv \ni \niobar \nis \nisd \Not
        \notchar \origof \parallel \parsim \perp \pitchfork \prec \Prec \precapprox \preccurlyeq \preceq \preceqq
        \precnapprox \precneq \precneqq \precnsim \rightfishtail \rightimply \righttail \risingdotseq \rsqhook
        \ruledelayed \scurel \shortdowntack \shortlefttack \shortmid \shortparallel \shortuptack \sim \simeq
        \simminussim \simneqq \simrdots \smallfrown \smallin \smallni \smallsmile \smeparsl \smile \stareq \succ \Succ
        \succapprox \succcurlyeq \succeq \succeqq \succnapprox \succneq \succneqq \succnsim \succsim \thickapprox
        \thicksim \topfork \upfishtail \upin \varisinobar \varisins \varniobar \varnis \varpropto \varVdash \vBar \Vbar
        \vBarv \Vdash \vdash
        \eqeq \eqeqeq \eqqsim \eqsim \equalparallel \equiv \Equiv \equivDD \equivVert \equivVvert
        \precsim \propto \prurel \pullback \pushout \questeq \revnmid \rfbowtie \rftimes \rightdbltail
        \vDash \VDash \vDdash \vdots \veeeq \veeonwedge \vertoverlay \vlongdash \Vvdash \wedgeq
        """
        # Table 105
        r"""
        \forks \napprox \napproxeqq \nasymp \nBumpeq \nbumpeq \ncong \ncongdot \ne \neqsim \nequiv \nhpar \nmid \nni
        \notin \nparallel \nprec \npreccurlyeq \npreceq \nshortmid \nshortparallel \nsim \nsime \nsucc \nsucccurlyeq
        \nsucceq \nvarisinobar \nvarniobar \nvDash \nvdash \nVDash \nVdash
        """
        # Table 106
        r"""
        \Colonapprox \colonapprox \coloneqq \Coloneqq \Coloneq \coloneq \colonsim \Colonsim \dblcolon \eqcolon \Eqcolon
        \eqqcolon \Eqqcolon
        """
        # Table 107
        r"""
        \dddtstile \ddststile \ddtstile \ddttstile \dndtstile \dnststile \dntstile \dnttstile \dsdtstile \dsststile
        \dststile \dsttstile \dtdtstile \dtststile \dttstile \dtttstile \nddtstile \ndststile \ndtstile \ndttstile
        \nndtstile \nnststile \nntstile \nnttstile \nsdtstile \nsststile \nststile \nsttstile \ntdtstile \ntststile
        \nttstile \ntttstile \sddtstile \sdststile \sdtstile \sdttstile \sndtstile \snststile \sntstile \snttstile
        \ssdtstile \ssststile \sststile \ssttstile \stdtstile \stststile \sttstile \stttstile \tddtstile \tdststile
        \tdtstile \tdttstile \tndtstile \tnststile \tntstile \tnttstile \tsdtstile \tsststile \tststile \tsttstile
        \ttdtstile \ttststile \tttstile \ttttstile
        """
        # Table 108
        r"""
        \InversTransformHoriz \InversTransformVert
        \TransformHoriz \TransformVert
        """
        # Table 109
        r"""
        \dfourier \fourier \laplace \ztransf \Dfourier \Fourier \Laplace \Ztransf
        """
        # Table 110
        r"""
        \coh \incoh \Perp \multimapboth \scoh \sincoh \simperp
        """
        # Table 111
        r"""
        \approxcolon \approxcoloncolon \colonapprox \coloncolon \coloncolonapprox \coloncolonequals \coloncolonminus
        \coloncolonsim \colonequals \colonminus \colonsim \equalscolon \equalscoloncolon \minuscolon \minuscoloncolon
        \ratio \simcolon \simcoloncolon
        """
        # Table 112
        r"""
        \nparallelslant \parallelslant
        """
        # Table 113
        r"""
        \sqsubset \sqsupseteq \supset \sqsubseteq \subset \supseteq \sqsupset \subseteq
        """
        # Table 114
        r"""
        \nsubseteq \nsupseteq \nsupseteqq \sqsubset \sqsupset \Subset \subseteqq \subsetneq \subsetneqq \Supset
        \supseteqq \supsetneq \supsetneqq \varsubsetneq \varsubsetneqq \varsupsetneq \varsupsetneqq
        """
        # Table 115
        r"""
        \subsetplus \subsetpluseq \supsetplus \supsetpluseq
        """
        # Table 116
        r"""
        \sqsubset \sqsupset
        """
        # Table 117
        r"""
        \nsqsubset \nsqsubseteq \nsqsupset
        \nsqsupseteq \nSubset \nsubseteqq
        \nSupset
        """
        # Table 118
        r"""
        \nsqsubset \nsqSubset \nsqsubseteq \nsqsubseteqq \nsqsupset \nsqSupset \nsqsupseteq \nsqsupseteqq \nsubset
        \nSubset \nsubseteq \nsubseteqq \nsupset \nSupset \nsupseteq \nsupseteqq \sqsubset \sqSubset \sqsubseteq
        \sqsubseteqq \sqsubsetneq \sqsubsetneqq \sqSupset \sqsupset \sqsupseteq \sqsupseteqq \sqsupsetneq \sqsupsetneqq
        \subset \Subset \subseteq \subseteqq \subsetneq \subsetneqq \supset \Supset \supseteq \supseteqq \supsetneq
        \supsetneqq \varsqsubsetneq \varsqsubsetneqq \varsqsupsetneq \varsqsupsetneqq \varsubsetneq \varsubsetneqq
        \varsupsetneq \varsupsetneqq
        """
        # Table 119
        r"""
        \nSqsubset \nsqsubset \nsqsubseteq \nsqsubseteqq \nSqsupset \nsqsupset \nsqsupseteq \nsqsupseteqq \nSubset
        \nsubset \nsubseteq \nsubseteqq \nSupset \nsupset \nsupseteq \nsupseteqq \Sasubset \sqsubset \sqsubseteq
        \sqsubseteqq \sqsubsetneq \sqsubsetneqq \Sqsupset \sqsupset \sqsupseteq \sqsupseteqq \sqsupsetneq \sqsupsetneqq
        \Subset \subset \subseteq \subseteqq \subsetneq \subsetneqq \Supset \supset \supseteq \supseteqq \supsetneq
        \supsetneqq \varsubsetneq \varsubsetneqq \varsupsetneq \varsupsetneqq
        """
        # Table 120
        r"""
        \nsqsubset \nSqsubset \nsqsubseteq \nsqsubseteqq \nsqsupset \nSqsupset \nsqsupseteq \nsqsupseteqq \nsubset
        \nSubset \nsubseteq \nsubseteqq \nsupset \nSupset \nsupseteq \nsupseteqq \sqsubset \Sqsubset \sqsubseteq
        \sqsubseteqq \sqsubsetneq \sqsubsetneqq \sqsupset \Sasupset \sqsupseteq \sqsupseteqq \sqsupsetneq \sqsupsetneqq
        \subset \Subset \subseteq \subseteqq \subsetneq \subsetneqq \supset \Supset \supseteq \supseteqq \supsetneq
        \supsetneqq \varsubsetneqq \varsubsetneq \varsupsetneqq \varsupsetneq
        """
        # Table 121
        r"""
        \nsubset \nsubseteq \nsubseteqq \nsupset \nsupseteq \nsupseteqq \sqsubset \sqSubset \sqSupset \sqsupset \Subset
        \subseteqq \subsetneq \subsetneqq \subsetplus \subsetpluseq \Supset \supseteqq \supsetneq \supsetneqq
        \supsetplus \supsetpluseq \varsubsetneq \varsubsetneqq \varsupsetneq \varsupsetneqq
        """
        # Table 122
        r"""
        \bsolhsub \csub \csube \csup \csupe \leftarrowsubset \nsqsubset \nsqsubseteq \nsqsupset \nsqsupseteq \nsubset
        \nsubseteq \nsubseteqg \nsupset \nsupseteq \nsupseteqq \rightarrowsupset \sqsubset \sqsubseteq \sqsubsetneq
        \sqsupset \sqsupseteq \sqsupsetneq \subedot \submult \subrarr \Subset \subset \subsetapprox \subsetcirc
        \subsetdot \subseteq \subseteqq \subsetneq \subsetneqq \subsetplus \subsim \subsub \subsup \supdsub \supedot
        \suphsol \suphsub \suplarr \supmult \Supset \supset \supsetapprox \supsetcirc \supsetdot \supseteq \supseteqq
        \supsetneq \supsetneqq \supsetplus \supsim \supsub \supsup \varsubsetneq \varsubsetneqq \varsupsetneq
        \varsupsetneqq
        """
        # Table 123
        r"""
        \geq \gg \leq \ll \neq
        """
        # Table 124
        r"""
        \eqslantgtr \eqslantless \geqq \geqslant \ggg \gnapprox \gneq \gneqq \gnsim \gtrapprox \gtrdot \gtreqless
        \gtreqqless \gtrless \gtrsim \gvertneqq \leqq \leqslant \lessapprox \lessdot \lesseggtr \lesseqggtr \lessgtr
        \lesssim \lll \lnapprox \lneq \lneqq \Insim \lvertneqq \ngeq \ngeqq \ngegslant \ngtr \nleq \nleqq \nleqslant
        \nless
        """
        # Table 125
        r"""
        \apprge \apprle
        """
        # Table 126
        r"""
        \ngg \ngtrapprox \ngtrless \ngtrsim \nlessapprox \nlessgtr \nlesssim \nll
        """
        # Table 127
        r"""
        \eqslantgtr \eqslantless \geq \geqq \gg \ggg \gnapprox \gneq \gneqq \gnsim \gtrapprox \gtrdot
        \gtreqless \gtreqqless \gtrless \gtrsim \gvertneqq \leq \leqq \lessapprox \lessdot \lesseqgtr \lesseqqgtr \lessgtr
        \lesssim \ll \lll \lnapprox \lneq \lneqq \lnsim \lvertneqq \neqslantgtr \neqslantless \ngeq \ngeqq
        \ngtr \ngtrapprox \ngtrsim \nleq \nleqq \nless \nlessapprox \nlesssim \nvargeq \nvarleq \vargeq \varleq
        \leqslant \le \geqslant \ge \nleqslant \ngeqslant
        """
        # Table 128
        r"""
        \eqslantgtr \eqslantless \geq \geclosed \geqdot \geqq \gegslant \geqslantdot \gg \ggg \gnapprox \gneqq \gns \im
        \gtr \gtrapprox \gtrclosed \gtrdot \gtreqless \gtreqlessslant \gtreqqless \gtrless \gtrneqqless \gtrsim \leq
        \leqclosed \leqdot \leqq \leqslant \legslantdot \less \lessapprox \lessclosed \lessdot \lesseqgtr
        \lesseqgtrslant \lesseqqgtr \lessgtr \lessneqggtr \lesssim \ll \lll \lnapprox \Ineqq \Insim \negslantgtr
        \neqslantless \ngeq \ngeqclosed \ngeqdot \ngeqq \ngeqslant \ngeqslantdot \ngg \nggg \ngtr \ngtrclosed \ngtrdot
        \ngtreqless \ngtreqlessslant \ngtreqqless \ngtrless \nleq \nleqclosed \nleqdot \nleqq \nleqslant \nlegslantdot
        \nless \nlessclosed \nlessdot \nlesseggtr \nlesseqgtrslant \nlesseqggtr \nlessgtr \nll \nlll \gggtr \gvertneqq
        \lhd \lless \lvertneqq \ntrianglelefteq \ntriangleleft \ntrianglerighteq \ntriangleright \rhd \trianglelefteq
        \trianglerighteq \unlhd \unrhd \vartriangleleft \vartriangleright
        """
        # Table 129
        r"""
        \eqslantgtr \eqslantless \geq \geqclosed \geqdot \geqq \geqslant \geqslantdot \geqslcc \gg \ggg \gnapprox \gneq
        \gneqq \gnsim \gtr \gtrapprox \gtrcc \gtrclosed \gtrdot \gtreqless \gtreqqless \gtreqslantless \gtrless \gtrsim
        \leq \leqclosed \leqdot \leqq \leqslant \leqslantdot \leqslcc \less \lessapprox \lesscc \lessclosed \lessdot
        \lesseqgtr \lesseqqgtr \lesseqslantgtr \lessgtr \lesssim \ll \lll \lnapprox \lneq \lneqq \lnsim \neqslantgtr
        \neqslantless \ngeq \ngeqclosed \ngeqdot \ngeqq \ngeqslant \ngeqslantdot \ngeqslcc \ngg \nggg \ngtr \ngtrapprox
        \ngtrcc \ngtrclosed \ngtrdot \ngtreqless \ngtreqqless \ngtreqslantless \ngtrless \ngtrsim \nleq \nleqclosed
        \nleqdot \nleqq \nlegslant \nleqslantdot \nleqslcc \nless \nlessapprox \nlesscc \nlessclosed \nlessdot
        \nlesseggtr \nlesseqggtr \nlesseqslantgtr \nlessgtr \nlesssim \nll \nlll \ge \gescc \gesdot \gesl \gggtr \gtcc
        \gtreqlessslant \gvertneqq \lesdot \lesg \lesseqgtrslant \lhd \llless \ltcc \lvertneqq \ngescc \ngtcc
        \ngtreqlessslant \nlescc \nlesdot \nlesg \nlesseqgtrslant \nltcc \rhd \le \lescc \ngesdot \ngesl \unlhd \unrhd
        """
        # Table 130
        r"""
        \eqslantgtr \egslantless \geqq \geqslant \ggg \glj \gnapprox \gneq \gneqq \gnsim \Gt \gtcir \gtrapprox
        \gtreqless \gtreqqless \gtrless \gtrsim \gvertneqq \leqq \legslant \lessapprox \lesseggtr \lesseqqgtr \lessgtr
        \lesssim \lll \lnapprox \lneq \Ineqq \lnsim \Lt \ltcir \lvertneqq \ngeq \ngeqq \ngeqslant \ngtr \nleq \nleqq
        \nleqslant \nless
        """
        # Table 131
        r"""
        \egsdot \elsdot \eqgtr \eqless \eqqgtr \eqqless \eqqslantgtr \eqqslantless \eqslantgtr \eqslantless \geq \geqq
        \geqqslant \geqslant \gescc \gesdot \gesdoto \gesdotol \gtquest \gtrapprox \gtrarr \gtrdot \gtreqless
        \gtreqqless \gtrless \gtrsim \gvertneqq \lat \late \leftarrowless \leq \leqq \leqqslant \legslant \lescc \lesdot
        \lnsim \lsime \lsimg \Lt \ltcc \ltcir \ltlarr \ltquest \lvertneqq \negslantgtr \negslantless \ngeq \ngeqq
        \ngeqslant \ngg \ngtr \ngtrless \ngtrsim \gesles \gg \ggg \gggnest \gla \glE \glj \gnapprox \gneq \gneqq \gnsim
        \gsime \gsiml \Gt \gtcc \gtcir \lesdoto \lesdotor \lesges \lessapprox \lessdot \lesseqgtr \lesseqqgtr \lessgtr
        \lesssim \lgE \ll \lll \lllnest \lnapprox \lneq \lneqq \nleq \nleqq \nleqslant \nless \nlessgtr \nlesssim \nll
        \partialmeetcontraction \rightarrowgtr \simgE \simgtr \simlE \simless \smt \smte \le \ge \llless \gggtr \nle
        \nge
        """
        # Table 132
        r"""
        \blacktriangleleft \blacktriangleright \ntriangleleft \ntrianglelefteq \ntriangleright \ntrianglerighteq
        \trianglelefteq \triangleq \trianglerighteq \vartriangleleft \vartriangleright
        """
        # Table 133
        r"""
        \trianglelefteqslant \ntrianglelefteqslant \trianglerighteqslant \ntrianglerighteqslant
        """
        # Table 134
        r"""
        \ntriangleleft \ntrianglelefteq \ntriangleright \ntrianglerighteq \triangleleft \trianglelefteq \triangleright
        \trianglerighteq \vartriangleleft \vartriangleright
        """
        # Table 135
        r"""
        \filledmedtriangledown \filledmedtriangleleft \filledmedtriangleright \filledmedtriangleup \filledtriangledown
        \filledtriangleleft \filledtriangleright \filledtriangleup \largetriangledown \largetriangleleft
        \largetriangleright \largetriangleup \medtriangledown \medtriangleleft \medtriangleright \medtriangleup
        \ntriangleeq \ntriangleleft \ntrianglelefteq \ntriangleright \ntrianglerighteq \otriangle \smalltriangledown
        \smalltriangleleft \smalltriangleright \smalltriangleup \triangleeq \trianglelefteq \trianglerighteq
        \vartriangleleft \vartriangleright \triangleq \lhd \lessclosed \rhd \gtrclosed \blacktriangledown
        \blacktriangleleft \blacktriangleright \blacktriangle \triangleright \trangle \vartriangle \bigtriangleup
        \triangleleft \triangledown \bigtriangledown \nlessclosed \ngtrclosed \nleqclosed \ngeqclosed
        """
        # Table 136
        r"""
        \geqclosed \gtrclosed \largetriangledown \largetriangleup \leqclosed \lessclosed \medblacktriangledown
        \medblacktriangleleft \medblacktriangleright \medblacktriangleup \medtriangledown \medtriangleleft
        \medtriangleright \medtriangleup \ngeqclosed \ngtrclosed \nleqclosed \nlessclosed \ntriangleeq
        \smallblacktriangledown \smallblacktriangleleft \smallblacktriangleright \smallblacktriangleup
        \smalltriangledown \smalltriangleleft \smalltriangleright \smalltriangleup \triangleeq \bigtriangledown
        \bigtriangleup \blacktriangle \blacktriangledown \blacktriangleleft \blacktriangleright \ntriangleleft
        \ntrianglelefteq \ntriangleright \trianglerighteq \triangle \triangledown \triangleleft \trianglelefteq
        \triangleq \triangleright \trianglerighteq \vartriangle \vartriangleleft \vartriangleright
        """
        # Table 137
        r"""
        \ntriangleleft \ntrianglelefteq \ntriangleright \ntrianglerighteq \triangleleft \lrtriangleeq \ltrivb
        \ntrianglelefteq \trianglelefteq \trianglelefteqslant \triangleright \trianglerighteq \trianglerighteqslant
        \varlrttriangle \vartriangle \vartriangleleft \vartriangleright
        """
        # Table 138
        r"""
        \lrtriangleeq \ltrivb \ntrianglelefteq \ntrianglerighteq \nvartriangleleft \nvartriangleright \rtriltri
        \trianglelefteq \triangleq \trianglerighteq \vartriangle \vartriangleleft \vartriangleright \vbrtri
        """
        # Table 139
        r"""
        \Downarrow \downarrow \hookleftarrow \hookrightarrow \leadsto \leftarrow \Leftarrow \Leftrightarrow
        \leftrightarrow \longleftarrow \Longleftarrow \longleftrightarrow \Longleftrightarrow \longmapsto
        \Longrightarrow \longrightarrow \mapsto \nearrow \nwarrow \Rightarrow \rightarrow \searrow \swarrow \uparrow
        \Uparrow \updownarrow \Updownarrow
        """
        # Table 140
        r"""
        \leftharpoondown \rightharpoondown \rightleftharpoons \leftharpoonup \rightharpoonup
        """
        # Table 142
        r"""
        \circlearrowleft \circlearrowright \curvearrowleft \curvearrowright \dashleftarrow \dashrightarrow
        \downdownarrows \leftarrowtail \leftleftarrows \leftrightarrows \leftrightsquigarrow \Lleftarrow \looparrowleft
        \looparrowright \Lsh \rightarrowtail \rightleftarrows \rightrightarrows \rightsquigarrow \Rsh \twoheadleftarrow
        \twoheadrightarrow \upuparrows
        """
        # Table 143
        r"""
        \nLeftarrow \nLeftrightarrow \nRightarrow \nleftarrow \nleftrightarrow \nrightarrow
        """
        # Table 144
        r"""
        \downharpoonleft \downharpoonright \leftrightharpoons \rightleftharpoons \upharpoonleft \upharpoonright
        """
        # Table 145
        r"""
        \leftarrowtriangle \leftrightarroweq \leftrightarrowtriangle \lightning \Longmapsfrom \longmapsfrom \Longmapsto
        \Mapsfrom \mapsfrom \Mapsto \nnearrow \nnwarrow \rightarrowtriangle \shortdownarrow \shortleftarrow
        \shortrightarrow \shortuparrow \ssearrow \sswarrow
        """
        # Table 146
        r"""
        \boxdotLeft \boxdotleft \boxdotright \boxdotRight \boxLeft \boxleft \boxright \boxRight \circleddotleft
        \circleddotright \circleleft \circleright \dashleftrightarrow \DiamonddotLeft \Diamonddotleft \Diamonddotright
        \DiamonddotRight \DiamondLeft \Diamondleft \Diamondright \DiamondRight \leftsquigarrow \Nearrow \Nwarrow
        \Rrightarrow \Searrow \Swarrow
        """
        # Table 147
        r"""
        \circlearrowleft \circlearrowright \curvearrowbotleft \curvearrowbotleftright \curvearrowbotright \curvearrowleft \curvearrowleftright \curvearrowright \dlsh \downdownarrows \downtouparrow \downuparrows \drsh
        \leftarrow \leftleftarrows \leftrightarrow \leftrightarrows \leftrightsquigarrow \leftsquigarrow \lefttorightarrow \looparrowdownleft \looparrowdownright \looparrowleft \looparrowright \Lsh \nearrow
        \nwarrow \restriction \rightarrow \rightleftarrows \rightrightarrows \rightsquigarrow \righttoleftarrow \Rsh \searrow \swarrow \updownarrows \uptodownarrow \upuparrows
        """
        # Table 148
        r"""
        \nLeftarrow \nleftarrow \nleftrightarrow \nLeftrightarrow \nrightarrow \nRightarrow
        """
        # Table 149
        r"""
        \barleftharpoon \barrightharpoon \downdownharpoons \downharpoonleft \downharpoonright \downupharpoons
        \leftbarharpoon \leftharpoondown \leftharpoonup \leftleftharpoons \leftrightharpoon \leftrightharpoons
        \rightbarharpoon \rightharpoondown \rightharpoonup \rightleftharpoon \rightleftharpoons \rightrightharpoons
        \updownharpoons \upharpoonleft \upharpoonright \upupharpoons
        """
        # Table 150
        r"""
        \curvearrowdownup \curvearrowleftright \curvearrownesw \curvearrownwse \curvearrowrightleft \curvearrowsenw
        \curvearrowswne \curvearrowupdown \dasheddownarrow \dashedleftarrow \dashednearrow \dashednwarrow
        \dashedrightarrow \dashedsearrow \dashedswarrow \dasheduparrow \Downarrow \downarrow \downarrowtail
        \downdownarrows \downlsquigarrow \downmapsto \downrsquigarrow \downuparrows \lcirclearrowdown \circlearrowleft
        \lcirclearrowright \lcirclearrowup \lcurvearrowdown \lcurvearrowleft \lcurvearrowne \lcurvearrownw
        \lcurvearrowright \lcurvearrowse \lcurvearrowsw \lcurvearrowup \Leftarrow \longleftarrow \Longleftarrow
        \longleftrightarrow \Longleftrightarrow \longmapsto \longrightarrow \Longrightarrow \looparrowleft
        \looparrowright \Lsh \nearrow \Nearrow \nearrowtail \nelsquigarrow \nemapsto \nenearrows \nersquigarrow
        \neswarrow \Neswarrow \neswarrows \nwarrow \Nwarrow \nwarrowtail \nwlsquigarrow \nwmapsto \nwnwarrows
        \nwrsquigarrow \nwsearrow \Nwsearrow \nwsearrows \partialvardlcircleleftint \partialvardlcirclerightint
        \partialvardrcircleleftint \partialvardrcirclerightint \partialvartlcircleleftint \partialvartlcirclerightint
        \partialvartrcircleleftint \rhookswarrow \rhookuparrow \rightarrow \Rightarrow \rightarrowtail \rightleftarrows
        \rightlsquigarrow \rightmapsto \rightrightarrows \rightrsquigarrow \Rrightarrow \Rsh \searrow \Searrow
        \searrowtail \selsquigarrow \semapsto \senwarrows \sersquigarrow \sesearrows \squigarrowdownup
        \squigarrowleftright \squigarrownesw \squigarrownwse \squigarrowrightleft \squigarrowsenw \squigarrowswne
        \squigarrowupdown \swarrow \Swarrow \swarrowtail \swlsquigarrow \swmapsto \swnearrows \swrsquigarrow \swswarrows
        \twoheaddownarrow \leftarrow \leftarrowtail \leftleftarrows \leftlsquigarrow \leftmapsto \leftrightarrow
        \Leftrightarrow \leftrightarrows \leftrsquigarrow \lhookdownarrow \lhookleftarrow \lhooknearrow \lhooknwarrow
        \lhookrightarrow \lhooksearrow \lhookswarrow \lhookuparrow \lightning \Lleftarrow \partialvartrcirclerightint
        \rcirclearrowdown \rcirclearrowleft \rcirclearrowright \rcirclearrowup \rcurvearrowdown \rcurvearrowleft
        \rcurvearrowne \rcurvearrownw \rcurvearrowright \rcurvearrowse \rcurvearrowsw \rcurvearrowup \rhookdownarrow
        \rhookleftarrow \rhooknearrow \rhooknwarrow \rhookrightarrow \rhooksearrow \twoheadleftarrow \twoheadnearrow
        \twoheadnwarrow \twoheadrightarrow \twoheadsearrow \twoheadswarrow \twoheaduparrow \uparrow \Uparrow
        \uparrowtail \updownarrow \Updownarrow \updownarrows \uplsquigarrow \upmapsto \uprsquigarrow \upuparrows
        \circlearrowleft \circlearrowright \curvearrowleft \curvearrowright \dashleftarrow \dashrightarrow
        \hookleftarrow \hookrightarrow \leadsto \leftrightsquigarrow \mapsto \rightsquigarrow
        """
        # Table 151
        r"""
        \ncurvearrowdownup \ncurvearrowleftright \ncurvearrownesw \ncurvearrownwse \ncurvearrowrightleft
        \ncurvearrowsenw \ncurvearrowswne \ncurvearrowupdown \nlhooknwarrow \nlhookrightarrow \nlhooksearrow
        \nlhookswarrow \nlhookuparrow \nLleftarrow \nnearrow \nNearrow \rightleftarrows \nrightlsquigarrow \nrightmapsto
        \nrightrightarrows \nrightrsquigarrow \nRrightarrow \nSearrow \nsearrow \ndasheddownarrow \ndashedleftarrow
        \ndashednearrow \ndashednwarrow \ndashedrightarrow \ndashedsearrow \ndashedswarrow \ndasheduparrow \ndownarrow
        \nDownarrow \ndownarrowtail \ndowndownarrows \ndownlsquigarrow \ndownmapsto \ndownrsquigarrow \ndownuparrows
        \nlcirclearrowdown \nlcirclearrowleft \nlcirclearrowright \nlcirclearrowup \nlcurvearrowdown \nlcurvearrowleft
        \nlcurvearrowne \nlcurvearrownw \nlcurvearrowright \nlcurvearrowse \nlcurvearrowsw \nlcurvearrowup \nLeftarrow
        \nleftarrow \nleftarrowtail \nleftleftarrows \nleftlsquigarrow \nleftmapsto \nleftrightarrow \nLeftrightarrow
        \nleftrightarrows \nleftrsquigarrow \nlhookdownarrow \nlhookleftarrow \nlhooknearrow \nnearrowtail
        \nnelsquigarrow \nnemapsto \nnenearrows \nnersquigarrow \nNeswarrow \nneswarrow \nneswarrows \nNwarrow \nnwarrow
        \nnwarrowtail \nnwlsquigarrow \nnwmapsto \nnwnwarrows \nnwrsquigarrow \nnwsearrow \nNwsearrow \nnwsearrows
        \nrcirclearrowdown \nrcirclearrowleft \nrcirclearrowright \nrcirclearrowup \nrcurvearrowdown \nrcurvearrowleft
        \nrcurvearrowne \nrcurvearrownw \nrcurvearrowright \nrcurvearrowse \nrcurvearrowsw \nrcurvearrowup
        \nrhookdownarrow \nrhookleftarrow \nrhooknearrow \nrhooknwarrow \nrhookrightarrow \nrhooksearrow \nrhookswarrow
        \nrhookuparrow \nrightarrow \nRightarrow \nrightarrowtail \nsearrowtail \nselsquigarrow \nsemapsto \nsenwarrows
        \nsersquigarrow \nsesearrows \nsquigarrowdownup \nsquigarrowleftright \nsquigarrownesw \nsquigarrownwse
        \nsquigarrowrightleft \nsquigarrowsenw \nsquigarrowswne \nsquigarrowupdown \nswarrow \nSwarrow \nswarrowtail
        \nswlsquigarrow \nswmapsto \nswnearrows \nswrsquigarrow \nswswarrows \ntwoheaddownarrow \ntwoheadleftarrow
        \ntwoheadnearrow \ntwoheadnwarrow \ntwoheadrightarrow \ntwoheadsearrow \ntwoheadswarrow \ntwoheaduparrow
        \nuparrow \nUparrow \nuparrowtail \nupdownarrow \nUpdownarrow \nupdownarrows \nuplsquigarrow \nupmapsto
        \nuprsquigarrow \nupuparrows \ncirclearrowleft \ncirclearrowright \ncurvearrowleft \ncurvearrowright \ndasharrow
        \ndashleftarrow \ndashrightarrow \ngets \nhookleftarrow \nhookrightarrow \nleadsto \nleftrightsquigarrow
        \nmapsto \nrightsquigarrow \nto
        """
        # Table 152
        r"""
        \downharpoonccw \downharpooncw \downupharpoons \leftharpooncow \leftharpooncw \leftrightharpoondownup
        \leftrightharpoons \leftrightharpoonupdown \neharpooncow \neharpooncw \neswharpoonnwse \neswharpoons
        \neswharpoonsenw \nwharpoonccw \nwharpooncw \nwseharpoonnesw \nwseharpoons \nwseharpoonswne \rightharpoonccw
        \rightharpooncw \rightleftharpoons \seharpoonccw \seharpooncw \senwharpoons \swharpoonccw \swharpooncw
        \swneharpoons \updownharpoonleftright \updownharpoonrightleft \updownharpoons \upharpooncow \upharpooncw
        \downharpoonup \downharpoondown \leftharpoonup \leftharpoondown \rightharpoonup \rightharpoondown \upharpoonup
        \upharpoondown \restriction
        """
        # Table 153
        r"""
        \ndownharpoonccw \ndownharpooncw \ndownupharpoons \nleftharpoonccw \nleftharpooncw \nleftrightharpoondownup
        \nleftrightharpoons \nleftrightharpoonupdown \nneharpoonccw \nneharpooncw \nneswharpoonnwse \ndownharpoonup
        \ndownharpoondown \nleftharpoonup \nleftharpoondown \nneswharpoons \nneswharpoonsenw \nnwharpoonccw
        \nnwharpooncw \nnwseharpoonnesw \nnwseharpoons \nnwseharpoonswne \nrightharpoonccw \nrightharpooncw
        \nrightleftharpoons \nseharpoonccw \nrightharpoonup \nrightharpoondown \nseharpooncw \nsenwharpoons
        \nswharpoonccw \nswharpooncw \nswneharpoons \nupdownharpoonleftright \nupdownharpoonrightleft \nupdownharpoons
        \nupharpoonccw \nupharpooncw \nupharpoonup \nupharpoondown \nrestriction
        """
        # Table 154
        r"""
        \acwcirclearrowdown \acwcirclearrowleft \acwcirclearrowright \acwcirclearrowup \acwleftarcarrow \acwnearcarrow
        \acwnwarcarrow \acwoverarcarrow \acwrightarcarrow \acwsearcarrow \acwswarcarrow \acwunderarcarrow
        \bdleftarcarrow \bdnearcarrow \bdnwarcarrow \bdoverarcarrow \bdrightarcarrow \bdsearcarrow \bdswarcarrow
        \bdunderarcarrow \cwcirclearrowdown \cwcirclearrowleft \cwcirclearrowright \cwcirclearrowup \cwleftarcarrow
        \cwnearcarrow \cwnwarcarrow \cwoverarcarrow \cwrightarcarrow \cwsearcarrow \cwswarcarrow \cwunderarcarrow
        \Ddownarrow \Downarrow \downarrow \downarrowtail \downbkarrow \downdownarrows \Downmapsto \downmapsto
        \downuparrows \downwavearrow \hookdownarrow \hookleftarrow \hooknearrow \hooknwarrow \hookrightarrow
        \hooksearrow \hookswarrow \hookuparrow \Ldsh \leftarrow \leftarrowtail \leftbkarrow \leftleftarrows \leftmapsto
        \Leftmapsto \Leftrightarrow \leftrightarrow \leftrightarrows \leftrightwavearrow \leftwavearrow \lightning
        \Lleftarrow \Longleftarrow \longleftarrow \longleftrightarrow \Longleftrightarrow \longleftwavearrow
        \Longmapsfrom \longmapsfrom \Longmapsto \longmapsto \longrightarrow \Longrightarrow \longrightwavearrow
        \looparrowleft \looparrowright \Lsh \nearrow \Nearrow \nearrowtail \nebkarrow \nenearrows \Neswarrow \neswarrow
        \neswarrows \Nwarrow \nwarrow \nwarrowtail \nwbkarrow \nwnwarrows \Nwsearrow \nwsearrow \nwsearrows \Rdsh
        \Rightarrow \rightarrow \rightarrowtail \rightbkarrow \rightleftarrows \Rightmapsto \rightrightarrows
        \rightwavearrow \Rrightarrow \Rsh \searrow \Searrow \searrowtail \sebkarrow \senwarrows \sesearrows \Swarrow
        \swarrow \swarrowtail \swbkarrow \swnearrows \swswarrows \twoheaddownarrow \twoheadleftarrow \twoheadnearrow
        \twoheadnwarrow \twoheadrightarrow \twoheadsearrow \twoheadswarrow \twoheaduparrow \uparrow \Uparrow
        \uparrowtail \upbkarrow \Updownarrow \updownarrow \updownarrows \updownwavearrow \upmapsto \Upmapsto \upuparrows
        \upwavearrow \Uuparrow \vardownwavearrow \varhookdownarrow \varhookleftarrow \varhooknearrow \varhooknwarrow
        \varhookrightarrow \varhooksearrow \varhookswarrow \varhookuparrow \varleftrightwavearrow \varleftwavearrow
        \varrightwavearrow \varupdownwavearrow \varupwavearrow \Leftarrow \Rightarrow \acwgapcirclearrow
        \acwopencirclearrow \circlearrowleft \circlearrowright \curvearrowleft \curvearrowright \cwgapcirclearrow
        \cwopencirclearrow \dasharrow \dashleftarrow \dashrightarrow \downlcurvearrow \downleftcurvedarrow
        \downlsquigarrow \downrcurvearrow \downrightcurvedarrow \downrsquigarrow \downupcurvearrow \downupsquigarrow
        \downzigzagarrow \gets \hknearrow \hknwarrow \hksearrow \hkswarrow \leadsto \leftcurvedarrow
        \leftdowncurvedarrow \leftlcurvearrow \leftlsquigarrow \leftrcurvearrow \leftrightcurvearrow
        \leftrightsquigarrow \leftrsquigarrow \leftsquigarrow \leftupcurvedarrow \lhookdownarrow \lhookleftarrow
        \lhooknearrow \lhooknwarrow \(lhookrightarrow \lhooksearrow \lhookswarrow \lhookuparrow \longleadsto
        \longleftsquigarrow \longrightsquigarrow \mapsdown \Mapsdown \mapsfrom \Mapsfrom \mapsto \Mapsto \mapsup \Mapsup
        \nelcurvearrow \nercurvearrow \neswcurvearrow \nwlcurvearrow \nwrcurvearrow \nwsecurvearrow \rhookdownarrow
        \rhookleftarrow \rhooknearrow \rhooknwarrow \rhookrightarrow \rhooksearrow \rhookswarrow \rhookuparrow
        \rightcurvedarrow \rightdowncurvedarrow \rightlcurvearrow \rightleftcurvearrow \rightleftsquigarrow
        \rightlsquigarrow \rightrcurvearrow \rightrsquigarrow \rightsquigarrow \rightupcurvedarrow \selcurvearrow
        \senwcurvearrow \sercurvearrow \swlcurvearrow \swnecurvearrow \swrcurvearrow \to \updowncurvearrow
        \updownsquigarrow \uplcurvearrow \upleftcurvedarrow \uplsquigarrow \uprcurvearrow \uprightcurvearrow
        \uprsquigarrow
        """
        # Table 155
        r"""
        \nacwcirclearrowdown \nacwcirclearrowleft \nacwcirclearrowright \nacwcirclearrowup \nacwleftarcarrow
        \nacwnearcarrow \nacwnwarcarrow \nacwoverarcarrow \nleftarrow \nLeftarrow \nleftarrowtail \nleftbkarrow
        \nleftleftarrows \nleftmapsto \nLeftmapsto \nleftrightarrow \nRrightarrow \nsearrow \nSearrow \nsearrowtail
        \nsebkarrow \nsenwarrows \nsesearrows \nswarrow \nacwrightarcarrow \nacwsearcarrow \nacwswarcarrow
        \nacwunderarcarrow \nbdleftarcarrow \nbdnearcarrow \nbdnwarcarrow \nbdoverarcarrow \nbdrightarcarrow
        \nbdsearcarrow \nbdswarcarrow \nbdunderarcarrow \ncwcirclearrowdown \ncwcirclearrowleft \ncwcirclearrowright
        \ncwcirclearrowup \ncwleftarcarrow \ncwnearcarrow \ncwnwarcarrow \ncwoverarcarrow \ncwrightarcarrow
        \ncwsearcarrow \ncwswarcarrow \ncwunderarcarrow \nDdownarrow \ndownarrow \nDownarrow \ndownarrowtail
        \ndownbkarrow \ndowndownarrows \ndownmapsto \nDownmapsto \ndownuparrows \ndownwavearrow \nhookdownarrow
        \nhookleftarrow \nhooknearrow \nhooknwarrow \nhookrightarrow \nhooksearrow \nhookswarrow \nhookuparrow
        \nLeftrightarrow \nleftrightarrows \nleftrightwavearrow \nleftwavearrow \nLleftarrow \nlongleftarrow
        \nLongleftarrow \nlongleftrightarrow \nLongleftrightarrow \nlongleftwavearrow \nlongmapsfrom \nLongmapsfrom
        \nlongmapsto \nLongmapsto \nlongrightarrow \nLongrightarrow \nlongrightwavearrow \nnearrow \nNearrow
        \nnearrowtail \nnebkarrow \nnenearrows \nneswarrow \nNeswarrow \nneswarrows \nnwarrow \nNwarrow \nnwarrowtail
        \nnwbkarrow \nnwnwarrows \nnwsearrow \nNwsearrow \nnwsearrows \nrightarrow \nRightarrow \nrightarrowtail
        \nrightbkarrow \nrightleftarrows \nrightmapsto \nRightmapsto \nrightrightarrows \nrightwavearrow \nSwarrow
        \nswarrowtail \nswbkarrow \nswnearrows \nswswarrows \ntwoheaddownarrow \ntwoheadleftarrow \ntwoheadnearrow
        \ntwoheadnwarrow \ntwoheadrightarrow \ntwoheadsearrow \ntwoheadswarrow \ntwoheaduparrow \nuparrow \nUparrow
        \nuparrowtail \nupbkarrow \nupdownarrow \nUpdownarrow \nupdownarrows \nupdownwavearrow \nupmapsto \nUpmapsto
        \nupuparrows \nupwavearrow \nUuparrow \nvardownwavearrow \nvarhookdownarrow \nvarhookleftarrow \nvarhooknearrow
        \nvarhooknwarrow \nvarhookrightarrow \nvarhooksearrow \nvarhookswarrow \nvarhookuparrow \nvarleftrightwavearrow
        \nvarleftwavearrow \nvarrightwavearrow \nvarupdownwavearrow \nvarupwavearrow \nacwgapcirclearrow
        \nacwopencirclearrow \ncirclearrowleft \ncirclearrowright \ncurvearrowleft \ncurvearrowright \ncwgapcirclearrow
        \ncwopencirclearrow \nleftdowncurvedarrow \nleftlcurvearrow \nleftlsquigarrow \nleftrcurvearrow
        \nleftrightcurvearrow \nleftrightsquigarrow \nleftrsquigarrow \nleftsquigarrow \nrightcurvedarrow
        \nrightdowncurvedarrow \nrightlcurvearrow \nrightleftcurvearrow \nrightleftsquigarrow \nrightlsquigarrow
        \nrightrcurvearrow \nrightrsquigarrow \ndasharrow \ndashleftarrow \ndashrightarrow \ndownlcurvearrow
        \ndownleftcurvedarrow \ndownlsquigarrow \ndownrcurvearrow \ndownrightcurvedarrow \ndownrsquigarrow
        \ndownupcurvearrow \ndownupsquigarrow \ngets \nhknearrow \nhknwarrow \nhksearrow \nhkswarrow \nleadsto
        \nleftcurvedarrow \nleftupcurvedarrow \nlongleadsto \nlongleftsquigarrow \nlongrightsquigarrow \nmapsdown
        \nMapsdown \nmapsfrom \nMapsfrom \nmapsto \nMapsto \nmapsup \nMapsup \nnelcurvearrow \nnercurvearrow
        \nneswcurvearrow \nnwlcurvearrow \nnwrcurvearrow \nnwsecurvearrow \nrightsquigarrow \nrightupcurvedarrow
        \nselcurvearrow \nsenwcurvearrow \nsercurvearrow \nswlcurvearrow \nswnecurvearrow \nswrcurvearrow \nto
        \nupdowncurvearrow \nupdownsquigarrow \nuplcurvearrow \nupleftcurvedarrow \nuplsquigarrow \nuprcurvearrow
        \nuprightcurvearrow \nuprsquigarrow
        """
        # Table 156
        r"""
        \downharpoonleft \downharpoonright \downupharpoons \leftharpoondown \leftharpoonup \leftrightharpoondownup
        \leftrightharpoons \leftrightharpoonupdown \neharpoonnw \neharpoonse \neswharpoonnwse \neswharpoons
        \neswharpoonsenw \nwharpoonne \nwharpoonsw \nwseharpoonnesw \nwseharpoons \nwseharpoonswne \rightharpoondown
        \rightharpoonup \rightleftharpoons \seharpoonne \seharpoonsw \senwharpoons \swharpoonnw \swharpoonse
        \swneharpoons \updownharpoonleftright \updownharpoonrightleft \updownharpoons \upharpoonleft \upharpoonright
        \restriction \updownharpoonsleftright \downupharpoonsleftright
        """
        # Table 157
        r"""
        \ndownharpoonleft \ndownharpoonright \ndownupharpoons \nleftharpoondown \nleftharpoonup \nleftrightharpoondownup \nleftrightharpoons \nleftrightharpoonupdown \nneharpoonnw \nneharpoonse \nneswharpoonnwse
        \nneswharpoons \nneswharpoonsenw \nnwharpoonne \nnwharpoonsw \nnwseharpoonnesw \nnwseharpoons \nnwseharpoonswne \nrightharpoondown \nrightharpoonup \nrightleftharpoons \nseharpoonne
        \nseharpoonsw \nsenwharpoons \nswharpoonnw \nswharpoonse \nswneharpoons \nupdownharpoonleftright \nupdownharpoonrightleft \nupdownharpoons \nupharpoonleft \nupharpoonright
        \nrestriction \ndownupharpoonsleftright \nupdownharpoonsleftright
        """
        # Table 158
        r"""
        \barleftarrow \barleftarrowrightarrowbar \barovernorthwestarrow \carriagereturn \circlearrowleft
        \circlearrowright \cupleftarrow \curlyveedownarrow \curlyveeuparrow \curlywedgedownarrow \curlywedgeuparrow
        \curvearrowbotleft \curvearrowbotleftright \curvearrowbotright \curvearrowleft \curvearrowleftright
        \curvearrowright \dlsh \downblackarrow \downdasharrow \downdownarrows \downtouparrow \downwhitearrow
        \downzigzagarrow \drsh \eqleftrightarrow \hookleftarrow \hookrightarrow \leftarrowtail \leftarrowTriangle \Lsh
        \mapsdown \Mapsfrom \mapsfrom \Mapsto \mapsto \mapsup \Nearrow \nearrowcorner \nnearrow \nnwarrow \Nwarrow
        \nwarrowcorner \rightarrowbar \rightarrowcircle \rightarrowtail \rightarrowTriangle \rightarrowtriangle
        \rightblackarrow \rightdasharrow \rightleftarrows \rightrightarrows \rightsquigarrow \rightthreearrows
        \righttoleftarrow \rightwhitearrow \rightwhiteroundarrow \Rrightarrow \Rsh \Searrow \leftarrowtriangle
        \leftblackarrow \leftdasharrow \leftleftarrows \leftrightarroweq \leftrightarrows \leftrightarrowTriangle
        \leftrightarrowtriangle \leftrightblackarrow \leftrightsquigarrow \leftsquigarrow \lefttorightarrow
        \leftwhitearrow \leftwhiteroundarrow \leftzigzagarrow \linefeed \Lleftarrow \looparrowdownleft
        \looparrowdownright \looparrowleft \looparrowright \ssearrow \sswarrow \Swarrow \twoheaddownarrow
        \twoheadleftarrow \twoheadrightarrow \twoheaduparrow \twoheadwhiteuparrow \twoheadwhiteuparrowpedestal
        \upblackarrow \updasharrow \updownarrowbar \updownblackarrow \updownwhitearrow \uptodownarrow \upuparrows
        \upwhitearrow \whitearrowupfrombar \whitearrowuppedestal \whitearrowuppedestalhbar \whitearrowuppedestalvbar
        """
        # Table 159
        r"""
        \nHdownarrow \nHuparrow \nLeftarrow \nleftarrow \nLeftrightarroW \nleftrightarrow \nLeftrightarrow \nrightarrow
        \nRightarrow \nVleftarrow \nVrightarrow
        """
        # Table 160
        r"""
        \downharpoonleft \downharpoonright \leftharpoondown \leftharpoonup \leftrightharpoons \rightharpoondown
        \rightharpoonup \rightleftharpoons \upharpoonleft \upharpoonright
        """
        # Table 161
        r"""
        \acwcirclearrow \acwgapcirclearrow \acwleftarcarrow \acwoverarcarrow \acwunderarcarrow \barleftarrow
        \barleftarrowrightarrowbar \barrightarrowdiamond \baruparrow \Absimilarleftarrow \bsimilarrightarrow
        \carriagereturn \ccwundercurvearrow \circlearrowleft \circlearrowright \circleonleftarrow \circleonrightarrow
        \curvearrowleft \curvearrowleftplus \curvearrowright \curvearrowrightminus \cwcirclearrow \cwgapcirclearrow
        \cwrightarcarrow \cwundercurvearrow \dbkarow \DDownarrow \Ddownarrow \diamondleftarrow \diamondleftarrowbar
        \downarrow \Downarrow \downarrowbar \downarrowbarred \downdasharrow \downdownarrows \downrightcurvedarrow
        \downuparrows \downwhitearrow \downzigzagarrow \draftingarrow \drbkarow \equalleftarrow \equalrightarrow
        \fdiagovnearrow \hknearrow \hknwarrow \hksearow \hkswarow \hookleftarrow \hookrightarrow \Ldsh \longmapsto
        \Longmapsto \longrightarrow \Longrightarrow \longrightsquigarrow \looparrowleft \looparrowright \Lsh \mapsdown
        \Mapsfrom \mapsfrom \mapsto \Mapsto \mapsup \Nearrow \nearrow \neovnwarrow  \neovsearrow  \neswarrow \nwarrow
        \Nwarrow \nwovnearrow  \nwsearrow \rdiagovsearrow  \Rdsh \Rightarrow \rightarrow \rightarrowapprox
        \rightarrowbackapprox \rightarrowbar \rightarrowbsimilar \rightarrowdiamond \rightarrowonoplus \rightarrowplus
        \rightarrowshortleftarrow \rightarrowsimilar \rightarrowtail \rightarrowtriangle \rightarrowx \rightbkarrow
        \rightcurvedarrow \rightdasharrow  \rightdotarrow \rightdowncurvedarrow \rightleftarrows \rightrightarrows
        \rightsquigarrow \rightthreearrows \rightwavearrow \rightwhitearrow  \RRightarrow \Rrightarrow \leftarrow
        \Leftarrow \leftarrowapprox \leftarrowbackapprox \leftarrowbsimilar \leftarrowonoplus \leftarrowplus
        \leftarrowshortrightarrow \leftarrowsimilar \leftarrowtail \leftarrowtriangle \leftarrowx \leftbkarrow
        \leftcurvedarrow \leftdasharrow \leftdbkarrow \leftdotarrow \leftdowncurvedarrow \leftleftarrows \Leftrightarrow
        \leftrightarrow \leftrightarrowcircle \leftrightarrows \leftrightarrowtriangle \leftrightsquigarrow
        \leftsquigarrow \leftthreearrows \leftwavearrow \leftwhitearrow \linefeed \LLeftarrow \Lleftarrow \longleftarrow
        \Longleftarrow \Longleftrightarrow \longleftrightarrow \longleftsquigarrow \Longmapsfrom \longmapsfrom \Rsh
        \searrow \Searrow \seovnearrow \shortrightarrowleftarrow \similarleftarrow \similarrightarrow \swarrow \Swarrow
        \toea \tona \tosa \towa \twoheaddownarrow \twoheadleftarrow \twoheadleftarrowtail \twoheadleftdbkarrow
        \twoheadmapsfrom \twoheadmapsto \twoheadrightarrow \twoheadrightarrowtail \twoheaduparrow \twoheaduparrowcircle
        \uparrow \Uparrow \uparrowbarred \updasharrow \Updownarrow \updownarrow \updownarrowbar \updownarrows
        \uprightcurvearrow \upuparrows \upwhitearrow \UUparrow \Uuparrow \varcarriagereturn \whitearrowupfrombar
        """
        # Table 162
        r"""
        \nHdownarrow \nHuparrow \nleftarrow \nLeftarrow \nleftrightarrow \nLeftrightarrow \nRightarrow \Nrightarrow
        \nvleftarrow \nvLeftarrow \nVleftarrow \nVleftarrowtail \nvleftarrowtail \nvleftrightarrow \nVleftrightarrow
        \nvLeftrightarrow \nVrightarrow \nvRightarrow \nvrightarrow \nVrightarrowtail \nvrightarrowtail
        \nvtwoheadleftarrow \nVtwoheadleftarrow \nvtwoheadleftarrowtail \nVtwoheadleftarrowtail \nVtwoheadrightarrow
        \nvtwoheadrightarrow \nvtwoheadrightarrowtail \nVtwoheadrightarrowtail \ngets
        """
        # Table 163
        r"""
        \bardownharpoonleft \bardownharpoonright \barleftharpoondown \barleftharpoonup \barrightharpoondown
        \barrightharpoonup \barupharpoonleft \barupharpoonright \dashleftharpoondown \dashrightharpoondown
        \downharpoonleft \downharpoonleftbar \downharpoonright \downharpoonrightbar \downharpoonsleftright
        \downupharpoonsleftright \leftharpoondown \leftharpoondownbar \leftharpoonsupdown \leftharpoonup
        \leftharpoonupbar \leftharpoonupdash \leftrightharpoondowndown \leftrightharpoondownup \leftrightharpoons
        \leftrightharpoonsdown \leftrightharpoonsup \leftrightharpoonupdown \leftrightharpoonupup \rightharpoondown
        \rightharpoondownbar \rightharpoonsupdown \rightharpoonup \rightharpoonupbar \rightharpoonupdash
        \rightleftharpoons \rightleftharpoonsdown \rightleftharpoonsup \updownharpoonleftleft \updownharpoonleftright
        \updownharpoonrightleft \updownharpoonrightright \updownharpoonsleftright \upharpoonleft \upharpoonleftbar
        \upharpoonright \upharpoonrightbar \upharpoonsleftright \restriction
        """
        # Table 165
        r"""
        \chemarrow
        """
        # Table 166
        r"""
        \fgerightarrow \fgeuparrow
        """
        # Table 167
        r"""
        \downarrow \hookleftarrow \hookrightarrow \leftarrow \leftrightarrow \longhookrightarrow \longleftarrow
        \longleftrightarrow \longmapsfrom \longmapsto \longrightarrow \mapsfrom \mapsto \nearrow \nwarrow \rightarrow
        \searrow \swarrow \uparrow \updownarrow \vardownarrow \varhookleftarrow \varhookrightarrow \varleftarrow
        \varleftrightarrow \varlonghookrightarrow \varlongleftarrow \varlongleftrightarrow \varlongmapsfrom
        \varlongmapsto \varlongrightarrow \varmapsfrom \varmapsto \varnearrow \varnwarrow \varrightarrow \varsearrow
        \varswarrow \varuparrow \varupdownarrow
        """
        # Table 168
        r"""
        \longleftharpoondown \longrightharpoondown \longleftharpoonup \longrightharpoonup
        """
        # Table 169
        r"""
        \restrictbarb \restrictbarbup \restrictmallet \restrictmalletup \restrictwand \restrictwandup
        """
        # Table 170
        r"""
        \downfilledspoon \downspoon \leftfilledspoon \leftspoon \ndownfilledspoon \ndownspoon \nefilledspoon \nespoon \nleftfilledspoon \nleftspoon \nnefilledspoon
        \nnespoon \nnwfilledspoon \nnwspoon \nrightfilledspoon \nrightspoon \nsefilledspoon \nsespoon \nswfilledspoon \nswspoon \nupfilledspoon \nupspoon
        \nwfilledspoon \nwspoon \rightfilledspoon \rightspoon \sefilledspoon \sespoon \swfilledspoon \swspoon \upfilledspoon \upspoon
        \multimap \nmultimap
        """
        # Table 171
        r"""
        \downpitchfork \leftpitchfork \ndownpitchfork \nepitchfork \nleftpitchfork \nnepitchfork \nnwpitchfork
        \nrightpitchfork \nsepitchfork \nswpitchfork \nuppitchfork \nwpitchfork \rightpitchfork \sepitchfork
        \swpitchfork \uppitchfork \pitchfork \npitchfork
        """
        # Table 172
        r"""
        \doublefrown \doublefrowneq \doublesmile \doublesmileeq \eqfrown \eqsmile \frown \frowneq \frowneqsmile
        \frownsmile \frownsmileeq \ndoublefrown \Indoublefrowneq \ndoublesmile \ndoublesmileeq \neqfrown \neqsmile
        \nfrown \nfrowneq \nfrowneqsmile \nfrownsmile \nfrownsmileeq \nsmile \nsmileeq \nsmileeqfrown \nsmilefrown
        \nsmilefrowneq \nsqdoublefrown \nsqdoublefrowneq \nsqdoublesmile \nsqdoublesmileeq \nsqeqfrown \nsqeqsmile
        \nsqfrown \nsqfrowneq \nsqfrowneqsmile \nsqfrownsmile \nsqsmile \nsqsmileeq \nsqsmileeqfrown \nsqsmilefrown
        \nsqtriplefrown \nsqtriplesmile \ntriplefrown \ntriplesmile \smile \smileeq \smileeqfrown \smilefrown
        \smilefrowneq \sqdoublefrown \sqdoublefrowneq \sqdoublesmile \sqdoublesmileeq \sqeqfrown \sqeqsmile \sqfrown
        \sqfrowneq \sqfrowneqsmile \sqfrownsmile \sqsmile \sqsmileeq \sqsmileeqfrown \sqsmilefrown \sqtriplefrown
        \striplesmile \triplefrown \triplesmile \smallsmile \smallfrown \asymp \nasymp
        """
        # Table 173
        r"""
        \blackwhitespoon \downblackspoon \downspoon \leftblackspoon \leftrightblackspoon \leftrightspoon \leftspoon
        \nblackwhitespoon \ndownblackspoon \ndownspoon \nleftblackspoon \nleftrightblackspoon \nleftrightspoon
        \nleftspoon \nrightblackspoon \nrightspoon \nupblackspoon \nupspoon \nwhiteblackspoon \rightblackspoon
        \rightspoon \upblackspoon \upspoon \whiteblackspoon \cirmid \dualmap \imageof \midcir \multimap \multimapinv
        \ncirmid \ndualmap \nimageof \nmidcir \nmultimap \nmultimapinv \norigof \origof
        """
        # Table 174
        r"""
        \downpitchfork \leftpitchfork \ndownpitchfork \nleftpitchfork \rightpitchfork \nrightpitchfork \uppitchfork
        \nuppitchfork
        """
        # Table 175
        r"""
        \frown \frowneq \frownsmile \nfrown \nfrowneq \nsmilefrown \nfrownsmile \smile \nsmile \nsmileeq \smileeq
        \smilefrown
        """
        # Table 176
        r"""
        \blitza \blitzb \blitzc \blitzd \blitze
        """
        # Table 203 (split)
        r"""
        \exists \forall \in \ni
        """
        # Table 204 (split)
        r"""
        \nexists
        """
        # Table 205 (partial)
        r"""
        \notin \notni
        """
        # Table 206 (split)
        r"""
        \barin \exists \in \nexists \notbot \notin \nowowner \nottop \owns \ownsbar \varnotin \varnotowner
        """
        # Table 207 (split)
        r"""
        \exists \forall \in \nexists \nin \nowns \owns \notin \ni
        """
        # Table 208 (split)
        r"""
        \exists \forall \in \nexists \nin \nowns \owns \notin \ni \nni
        """
        # Table 209 (split)
        r"""
        \nexists
        """
        # Table 212
        r"""
        \in \notin \notsmallin \notsmallowns \owns \smallin \smallowns
        """
        # Table 227 (split)
        r"""
        \parallel \mVert
        """
        # Table 302 (split)
        r"""
        \neg
        """
        # Table 307 (partial)
        r"""
        \backneg \invneg \neg \lnot \minushookdown \minushookup \hookdownminus \hookupminus
        """
        # Table 309 (partial)
        r"""
        \backneg \intprod \intprodr \invneg \neg \hookdownminus \invneg \invnot \long \minushookdown
        \hookupminus \turnedbackneg \minushookup \turnedneg \turnednot
        """
    ).split()
)

letter_symbols = set(
    (
        # Table 187
        r"""
        \Complex \COMPLEX \Integer \INTEGER \Natural \NATURAL \Rational \RATIONAL \Real \REAL
        """
        # Table 188
        r"""
        \alpha \beta \gamma \delta \epsilon \varepsilon \zeta \eta \Gamma \Delta \Theta \theta \vartheta \iota \kappa
        \lambda \mu \nu \xi \Lambda \Xi \Pi \pi \varpi \rho \varrho \sigma \varsigma \Sigma \Upsilon \Phi \tau \upsilon
        \phi \varphi \chi \psi \omega \Psi \Omega \Alpha \Beta \Epsilon \Zeta \Eta \Iota \Kappa \Mu \Nu \Omiron \Rho
        \Tau \Chi \omicron
        """
        # Table 189
        r"""
        \digramma varkappa
        """
        # Table 190
        r"""
        \alphaup \betaup \gammaup \deltaup \epsilonup \varepsilonup \zetaup \etaup \thetaup \varthetaup \iotaup \kappaup
        \lambdaup \muup \nuup \xiup \piup \varpiup \rhoup \varrhoup \sigmaup \varsigmaup \tauup \upsilonup \phiup
        \varphiup \chiup \psiup \omegaup
        """
        # Table 191
        r"""
        \upalpha \upbeta \upgamma \updelta \upepsilon \upvarepsilon \upzeta \upeta \Upgamma \Updelta \Uptheta \uptheta
        \upvartheta \upiota \upkappa \uplambda \upmu \upnu \upxi \Uplambda \Upxi \Uppi \uppi \upvarpi \uprho \upvarrho
        \upsigma \upvarsigma \uptau \upupsilon \Upsigma \Upupsilon \Upphi \upphi \upvarphi \upchi \uppsi \upomega \Uppsi
        \Upomega
        """
        # Table 192
        r"""
        \pi \rho \varphi \varrho \varvarpi \varvarrho
        """
        # Table 193
        r"""
        \varg \varv \varw \vary
        """
        # Table 194
        r"""
        \varbeta \varepsilon \varkappa \varphi \varpi \varrho \varsigma \vartheta
        """
        # Table 195
        r"""
        \varg
        """
        # Table 196
        r"""
        \varepsilon \varkappa \varphi \varpi \varrho \varsigma \vartheta
        """
        # Table 197
        r"""
        \backepsilon \mho \turnediota \upbackepsilon
        """
        # Table 198
        r"""
        \beth \gimel \daleth
        """
        # Table 199
        r"""
        \aleph \beth \gimel \daleth
        """
        # Table 200
        r"""
        \aleph \beth \gimel \daleth
        """
        # Table 201
        r"""
        \beth \gimel daleth
        """
        # Table 202
        r"""
        \aleph \beth \gimel \daleth
        """
        # Table 203 (split)
        r"""
        \bot \ell \hbar \imath \jmath \top \
        """
        # Table 204 (split)
        r"""
        \Bbbk \hbar \hslash \circledR \circledS \Finv \Game
        """
        # Table 207 (split)
        r"""
        \bot \top \intercal
        """
        # Table 208 (split)
        r"""
        \bot \hbar \hslash \top
        """
        # Table 209 (split)
        r"""
        \Bbbk \hbar \hslash \imath \jmath
        """
        # Table 210 (partial)
        r"""
        \digamma \ell \Eulerconst \topbot \Yup Zbar
        """
        # Table 211 (partial)
        r"""
        \e
        """
        # Table 215
        r"""
        \Bot \simbot
        """
        # Table 302 (split)
        r"""
        \aleph \emptyset \infty
        """
        # Table 303 (partial)
        r"""
        \varnothing
        """
        # Table 309 (partial)
        r"""
        \varnothing \emptyset \infty
        """
    ).split()
)

generic_delims = set(
    (
        # Table 216
        r"""
        \ulcorner \llcorner \urcorner \lrcorner
        """
        # Table 217
        r"""
        \Lbag \llceil \llparenthesis \Rbag \rrceil \rrparenthesis \lbag \llfloor \rbag \rrfloor
        """
        # Table 218
        r"""
        \lcorners \ulcorner \llcorner \rcorners \urcorner \lrcorner
        """
        # Table 219
        r"""
        \ulcorner \llcorner \urcorner \lrcorner
        """
        # Table 220
        r"""
        \langledot \lbag \lblkbrbrak \lbracklltick \lbrackubar \lbrackultick \Lbrbrak \lcurvyangle
        \rangledot \rbag \rblkbrbrak \rbrackurtick \rbrackubar \rbracklrtick \Rbrbrak \rcurvyangle
        \llangle \llcorner \llparenthesis \Lparengtr \lparenless \lvzigzag \Lvzigzag \ulcorner
        \rrangle \lrcorner \rrparenthesis \Rparenless \rparengtr \rvzigzag \Rvzigzag \urcorner
        """
        # Table 221
        r"""
        \niv \vin
        """
        # Table 222
        r"""
        \downarrow \langle \lceil \lfloor \Downarrow \rangle \rceil \rfloor \uparrow \updownarrow \| \Uparrow
        \Updownarrow
        """
        # Table 223
        r"""
        \lmoustache \rmoustache \arrowvert \Arrowvert \bracevert
        """
        # Table 224
        r"""
        \lvert \rvert \lVert \rVert
        """
        # Table 225
        r"""
        \llbracket \rrbracket
        """
        # Table 226
        r"""
        \ldbrack \rdbrack \lfilet \rfilet \thinkvert \vvert
        """
        # Table 227
        r"""
        \Arrowvert \arrowvert \backslash \bracevert \lceil \lfloor \llangle \llcorner \lmoustache \Ircorner \lsem
        \lwavy \lWavy \rangle \rceil \rfloor \rmoustache \rrangle \rsem \rWavy \rwavy \ulcorner \ullcorner \ulrcorner
        \urcorner \langle \ranglebar \| \langlebar \Vert
        """
        # Table 228
        r"""
        \backslash \downarrow \Downarrow \lAngle \langle \langledot \lBrack \lrcorner \lvert \lVert \lVvert \mathslash
        \rangle \rAngle \rangledot \rvert \rVert \rVvert \ulcorner \ullcorner \ulrcorner \uparrow \Uparrow \lceil
        \lfloor \llcorner \lmoustache \rBrack \rceil \rfloor \rmoustache \updownarrow \Updownarrow \urcorner \Vert
        \Vvert
        """
        # Table 229
        r"""
        \Arrowvert \arrowvert \backslash \Ddownarrow \DDownarrow \lAngle \lBrace \lBrack \lbrbrak \rceil \rfloor
        \rmoustache \downarrow \Downarrow \langle \lceil \lfloor \lmoustache \lParen \rAngle \rangle \rBrace \rBrack
        \rbrbrak \uparrow \Uparrow \Updownarrow \updownarrow \Uuparrow \UUparrow \Vert \Vvert
        """
        # Table 230
        r"""
        \leftwave \rightwave \leftevaw \rightevaw
        """
        # Table 231
        r"""
        \lAngle \lBrack \rAngle \rBrack \lCeil \lFloor \rCeil \rFloor \lVert  \rVert
        """
        # Table 233
        r"""
        \llbracket \rrbracket \VERT
        """
    ).split()
)

vert = set(
    (
        # Table ???
        r"""
    |
    """
        # Table 227
        r"""
    \vert
    """
        # Table 228
        r"""
    \vert
    """
    ).split()
)


left_parens = set(
    (
        # Table 222
        r"""
    (
    """
        # Table 223
        r"""
    \lgroup
    """
        # Table 227
        r"""
    \lgroup
    """
        # Table 228
        r"""
    \lparen \lgroup
    """
    ).split()
)

right_parens = set(
    (
        # Table 222
        r"""
    )
    """
        # Table 223
        r"""
    \rgroup
    """
        # Table 227
        r"""
    \rgroup
    """
        # Table 228
        r"""
    \rparen \rgroup
    """
    ).split()
)

left_brace = set(
    (
        # Table 222
        r"""
    \{
    """
        # Table 227
        r"""
    \lbrace
    """
        # Table 228
        r"""
    \lbrace
    """
    ).split()
)

right_brace = set(
    (
        # Table 222
        r"""
    \}
    """
        # Table 227
        r"""
    \rbrace
    """
        # Table 228
        r"""
    \rbrace
    """
    ).split()
)

left_bracket = set(
    (
        # Table 222
        r"""
    [
    """
        # Table 228
        r"""
    \lbrack
    """
    ).split()
)

right_bracket = set(
    (
        # Table 222
        r"""
    ]
    """
        # Table 228
        r"""
    \lbrack
    """
    ).split()
)
