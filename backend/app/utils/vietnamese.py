# backend/app/utils/vietnamese.py
def format_food_name_with_accent(name: str) -> str:
    """
    Format tên món ăn có dấu (cho web)
    VD: 'Banh mi' -> 'Bánh mì'
    """
    # Mapping các món ăn phổ biến
    FOOD_NAME_MAPPING = {
        # EfficientNet classes
        'Banh beo': 'Bánh bèo',
        'Banh bot loc': 'Bánh bột lọc',
        'Banh can': 'Bánh căn',
        'Banh canh': 'Bánh canh',
        'Banh chung': 'Bánh chưng',
        'Banh cuon': 'Bánh cuốn',
        'Banh duc': 'Bánh đúc',
        'Banh gio': 'Bánh giò',
        'Banh khot': 'Bánh khọt',
        'Banh mi': 'Bánh mì',
        'Banh pia': 'Bánh pía',
        'Banh tet': 'Bánh tét',
        'Banh trang nuong': 'Bánh tráng nướng',
        'Banh xeo': 'Bánh xèo',
        'Bun bo Hue': 'Bún bò Huế',
        'Bun dau mam tom': 'Bún đậu mắm tôm',
        'Bun mam': 'Bún mắm',
        'Bun rieu': 'Bún riêu',
        'Bun thit nuong': 'Bún thịt nướng',
        'Ca kho to': 'Cá kho tộ',
        'Canh chua': 'Canh chua',
        'Cao lau': 'Cao lầu',
        'Chao long': 'Cháo lòng',
        'Com tam': 'Cơm tấm',
        'Goi cuon': 'Gỏi cuốn',
        'Hu tieu': 'Hủ tiếu',
        'Mi quang': 'Mì quảng',
        'Nem chua': 'Nem chua',
        'Pho': 'Phở',
        'Xoi xeo': 'Xôi xéo',
        
        # Keras classes
        'banh_mi_ap_chao': 'Bánh mì áp chảo',
        'banh_xeo_hai_san': 'Bánh xèo hải sản',
        'bun_gio_heo': 'Bún giò heo',
        'ca_bong_trung_kho_tieu': 'Cá bống trứng kho tiêu',
        'canh_chua_ca': 'Canh chua cá',
        'canh_kho_qua_ham_thit': 'Canh khổ qua hầm thịt',
        'chan_ga_xa_ot': 'Chân gà xả ớt',
        'chao_ca_nau_bap_nep': 'Cháo cá nấu bắp nếp',
        'com_chien': 'Cơm chiên',
        'dau_hu_xot_cay': 'Đậu hủ xốt cay',
        'ech_xao_lan': 'Ếch xào lăn',
        'ga_hap_hanh': 'Gà hấp hành',
        'ga_nuong': 'Gà nướng',
        'luon_xao_xa_ot': 'Lươn xào xả ớt',
        'ngheu_hap_thai': 'Nghêu hấp Thái',
        'pizza_hai_san': 'Pizza hải sản',
        'sup_ga_bi_do': 'Súp gà bí đỏ',
        'thit_kho': 'Thịt kho',
        'trung_chien_rau_cu_xot_mayonnaise': 'Trứng chiên rau củ xốt mayonnaise',
        'vit_kho_rieng': 'Vịt kho riềng',
    }
    
    return FOOD_NAME_MAPPING.get(name, name)