# Film Öneri Sistemi Projesi

Bu proje, [MovieLens 20M](https://grouplens.org/datasets/movielens/20m/) veri setini kullanarak bir film öneri sistemi geliştirmeyi amaçlamaktadır. Proje, kullanıcıların geçmişteki izleme geçmişine dayanarak film önerileri sunmayı hedeflemektedir.

## Proje Hakkında

Film öneri sistemi, kullanıcılara en çok ilgilerini çekebilecek filmleri önermek için Apriori algoritmasını kullanmaktadır. Proje aşağıdaki aşamalardan oluşmaktadır:

1. **Veri Temizleme**: Ham verinin analizi ve eksik verilerin işlenmesi.
2. **Veri Dönüştürme**: Verinin uygun formata dönüştürülmesi.
3. **Apriori Algoritması**: Sık kullanılan film gruplarının ve ilişki kurallarının belirlenmesi.
4. **Öneri Sistemi Oluşturma**: Kullanıcılara öneri sunmak için bir arayüz tasarımı.

## Kullanılan Teknolojiler

- **Python**: Proje dili
- **Pandas**: Veri analizi için
- **mlxtend**: Apriori algoritması ve ilişki kuralları için
- **Tkinter**: GUI oluşturmak için (isteğe bağlı)

## Katkıda Bulunma

Herhangi bir katkı veya öneriniz varsa, lütfen bir pull request oluşturun veya sorularınızı açıkça belirtin.
Bu şablonu kendi projenin özelliklerine göre düzenleyebilirsin. README dosyası,
projenin amacını ve nasıl çalıştığını açıklamak için önemli bir belge olduğundan, gerekli bilgileri net bir şekilde vermeye çalıştım. Başka bir şey eklemek veya değiştirmek istersen, bana bildirebilirsin!


## Kurulum

Projenin çalışabilmesi için gerekli kütüphaneleri yüklemek için aşağıdaki komutları kullanın:

```bash
pip install pandas mlxtend



