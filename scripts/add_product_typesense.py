import typesense

HOST = "6fu5w7p0ksgon83zp-1.a1.typesense.net"
TYPESENSE_API_KEY = "I1v85264rZoL6r11vh3BNZkuQDQqcN7n"

typesense_client = typesense.Client({
    "nodes": [{
        "host": HOST,
        "port": "443",
        "protocol": "https"
    }],
    "api_key": TYPESENSE_API_KEY,
    "connection_timeout_seconds": 180
})



products = [{'id': '52c9398c-a530-40f7-9071-d665f0d5071e', 'name': 'Intel Xeon W-3400', 'description': 'Workstation and server CPUs with high core counts, designed for professional workloads like 3D rendering and data processing.', 'price': 1000.0, 'discount_percent': 0.0, 'brand': 'Intel', 'stock': 20, 'sold': 0, 'category_name': 'CPU', 'product_rating': 0, 'embedding': [-0.060579292476177216, 0.032939374446868896, -0.03671036288142204, -0.027417100965976715, -0.002433203626424074, -0.07285378128290176, 0.03953830897808075, 0.06262581050395966, 0.012529365718364716, -0.03455200418829918, 0.0561637282371521, -0.022001683712005615, 0.0421011857688427, 0.0015780110843479633, -0.05600510165095329, 0.039489660412073135, 0.11080186814069748, -0.09842777997255325, 0.05004102364182472, -0.050065066665410995, -0.0014367757830768824, 0.012719972990453243, -0.05832764506340027, -0.004317809361964464, 0.09345068037509918, 0.08532862365245819, 0.05633862316608429, -0.08111904561519623, -0.02458062954246998, -0.010949643328785896, -0.03998088836669922, -0.05142601951956749, 0.05633866414427757, 0.04941286891698837, 0.06533204019069672, -0.036807551980018616, 0.02361563965678215, -0.057954855263233185, -0.02218855917453766, -0.058882106095552444, -0.031995948404073715, -0.0537802055478096, -0.02371172234416008, 0.09066243469715118, -0.00035635524545796216, 0.061004094779491425, -0.04011224955320358, -0.044994935393333435, -0.020534435287117958, 0.06735968589782715, -0.02290789596736431, -0.05814862251281738, -0.032366182655096054, -0.0025315899401903152, 0.01747913472354412, -0.029183218255639076, 0.046019233763217926, -0.0223408080637455, -0.001391866710036993, 0.0017915352946147323, 0.05767546966671944, -0.11801190674304962, 0.024079881608486176, 0.059740100055933, 0.03226620703935623, -0.05129285156726837, -0.0008231880492530763, -0.07779403775930405, 0.01577959954738617, -0.05286663770675659, 0.05255359038710594, -0.004220009781420231, 0.04070799797773361, -0.04173744469881058, -0.08131782710552216, -0.01771523989737034, 0.09794282913208008, -0.10734836012125015, 0.050965044647455215, -0.02008606120944023, -0.0035835711751133204, 0.013188743963837624, -0.033690277487039566, -0.04210484400391579, 0.0896156057715416, -0.040099550038576126, -0.005964812822639942, -0.006358178798109293, 0.018141260370612144, -0.07276053726673126, -0.031059592962265015, -0.004408850334584713, -0.04998287558555603, -0.022209106013178825, 0.012617870233952999, 0.0048095486126840115, 0.04830753058195114, -0.05962230637669563, -0.006787522695958614, 0.04213764891028404, -0.02842334844172001, -0.01513367984443903, 0.12165563553571701, 0.0006094826385378838, -0.06585580110549927, -0.03731834515929222, -0.035509075969457626, 0.0973534882068634, -0.09312184900045395, -0.0374310128390789, -0.08425842970609665, -0.044971343129873276, -0.07222823053598404, 0.03340509161353111, 0.045204464346170425, -0.06260470300912857, 0.06055263429880142, 0.03703157231211662, 0.042963895946741104, 0.02834697999060154, 0.028273792937397957, -0.08511704206466675, -0.04332687333226204, -0.026398878544569016, -0.06574220955371857, -0.06997764855623245, -0.055524349212646484, 2.080383289929561e-33, 0.018216747790575027, 0.09176160395145416, -0.0947301983833313, -0.09186574071645737, 0.021733731031417847, -0.03688511997461319, 0.014599359594285488, 0.031338222324848175, -0.016186974942684174, 0.12736724317073822, -0.05760766938328743, 0.008686451241374016, 0.03351527079939842, 0.09361708909273148, 0.021894775331020355, -0.10851053893566132, 0.024419231340289116, 0.07547076791524887, 0.026713097468018532, 0.03247081860899925, 0.02813575230538845, -0.020266393199563026, -0.013774205930531025, -0.04408228024840355, -0.01079082302749157, 0.048665255308151245, -0.021662700921297073, -0.05924558266997337, 0.07508670538663864, 0.01761256530880928, 0.03138231113553047, -0.0760686844587326, 0.00236697681248188, -0.08817965537309647, -0.014676530845463276, 0.04914544150233269, -0.04528427496552467, -0.10783293098211288, 0.012841401621699333, 0.0063550882041454315, -0.03414841741323471, 0.09433525800704956, -0.03927795588970184, -0.007886407896876335, 0.011072457768023014, 0.017339730635285378, -0.03615039587020874, -0.051278457045555115, 0.00396632868796587, -0.014682723209261894, -0.036222003400325775, 0.044386446475982666, -0.013956944458186626, 0.0012811744818463922, 0.021374667063355446, -0.017661655321717262, 0.05494540184736252, 0.10087034106254578, 0.05246049538254738, 0.14128519594669342, -0.060498856008052826, -0.02422681637108326, -0.06750311702489853, -0.03204163536429405, -0.010219006799161434, 0.028376379981637, 0.07444550842046738, 0.07348965108394623, -0.06364964693784714, 0.087697334587574, -0.04610206186771393, -0.0828661099076271, 0.1008741706609726, -0.02187550999224186, 0.023118525743484497, 0.027119489386677742, -0.08011691272258759, -0.06779315322637558, -0.08551522344350815, -0.05353197827935219, -0.05209750682115555, 0.014162443578243256, 0.020982062444090843, -0.007709012366831303, -0.003973625600337982, 0.08231976628303528, -0.10577201098203659, 0.04882490634918213, -0.014965451322495937, 0.0389891155064106, 0.020565243437886238, 0.05838072672486305, 0.017829952761530876, 0.00790600199252367, -0.033784419298172, -2.5444603781105383e-33, -0.05186138302087784, -0.015261898748576641, -0.004275173414498568, 0.06560099869966507, 0.025677543133497238, 0.003428214229643345, -0.06376057863235474, 0.008046600967645645, -0.04680773988366127, 0.05247264727950096, 0.045141227543354034, 0.007527532521635294, -0.0023603502195328474, 0.0724661573767662, 0.007789937313646078, 0.051715362817049026, -0.054620083421468735, -0.07869983464479446, 0.022456806153059006, -0.011925267055630684, -0.005735090468078852, 0.10682065039873123, 0.003492460586130619, -0.04323413595557213, -0.028826294466853142, 0.043823979794979095, -0.03926580026745796, 0.01419370248913765, 0.10154558718204498, -0.02123459056019783, -0.08425494283437729, -0.10050208121538162, 0.07690510898828506, 0.020152967423200607, 0.06393260508775711, -0.022135300561785698, 0.06137801334261894, -0.003812058363109827, -0.010102378204464912, 0.04687749966979027, 0.07657114416360855, 0.023923173546791077, 0.011317846365272999, 0.0775875672698021, -0.008191805332899094, 0.04269495606422424, -0.0001345719792880118, -0.09241710603237152, 0.06374794244766235, -0.010357767343521118, -0.017777923494577408, -0.03506145626306534, 0.026235459372401237, 0.0346103236079216, -0.07456432282924652, -0.060368772596120834, -0.04575047269463539, 0.09444380551576614, 0.022871723398566246, -0.052094340324401855, 0.03325940668582916, 0.012225319631397724, 0.009768493473529816, 0.05323133245110512, 0.0716598778963089, 0.02521449513733387, 0.03399796411395073, 0.00673165637999773, -0.05531320720911026, -0.04173924773931503, -0.01262239646166563, -0.02999953366816044, 0.0028371436055749655, -0.014913750812411308, -0.036203525960445404, -0.0063223582692444324, 0.015160740353167057, -0.03712337091565132, 0.043274037539958954, 0.011724154464900494, 0.03705935552716255, 0.015985053032636642, 0.03579500690102577, 0.0020182759035378695, 0.020979953929781914, -0.06521223485469818, -0.0055567920207977295, 0.041751179844141006, -0.07666156440973282, -0.05262850970029831, -0.09996464103460312, 0.0014488539891317487, -0.01770278625190258, -0.018547989428043365, -0.03587300330400467, -3.076136323443279e-08, 0.03000033088028431, -0.012501582503318787, 0.06578386574983597, 0.04037848487496376, 0.0028146118856966496, -0.03928418084979057, 0.03973589837551117, -0.011520549654960632, 0.039804913103580475, 0.02567109651863575, 0.05401184409856796, -0.13754746317863464, -0.0022614167537540197, -0.028190767392516136, 0.0721774697303772, 0.012812240049242973, -0.019189290702342987, 0.07885576039552689, 0.027559740468859673, -0.01863683946430683, -0.00515297194942832, 0.058464184403419495, 0.07631656527519226, -0.05573870614171028, -0.06682177633047104, 0.05139021575450897, 0.029817640781402588, 0.0496746301651001, -0.0037649215664714575, -0.030766932293772697, -0.07693877071142197, 0.06944414973258972, 0.0738486722111702, -0.024273300543427467, 0.06194615736603737, -0.0027875101659446955, -0.03003162145614624, 0.04608425870537758, 0.07109517604112625, 0.036340922117233276, -0.08132820576429367, -0.02763843908905983, -0.06278258562088013, 0.007514236960560083, 0.09044646471738815, 0.05308593437075615, -0.08857375383377075, -0.10491791367530823, -0.014781974256038666, 0.03262171149253845, -0.012107896618545055, 0.016087260097265244, 0.021022526547312737, 0.025318659842014313, -0.018583407625555992, 0.02794196642935276, -0.008425411768257618, -0.025419535115361214, 0.020398497581481934, 0.06577014178037643, 0.05393452197313309, -0.0960482507944107, 0.0062158312648534775, -0.031410299241542816]}]



res = typesense_client.collections["products-collection"].documents.import_(products, {'action': 'upsert'})
# res = typesense_client.collections['products-collection'].documents.export()

print(res)