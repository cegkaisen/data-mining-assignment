## **1. Introduction**

Git repository link: 

Bu çalışmada verilen market alışveriş veri seti üzerinde association rule mining yaptım. Association rule mining, transaction verileri içinde birlikte sık görülen item’ları ve bunlar arasındaki ilişkileri bulmak için kullanılan bir data mining yöntemidir. Bu yöntem özellikle market basket analysis için kullanılır. Müşterilerin alışveriş sepetlerinde hangi ürün kategorilerinin birlikte satın alındığını incelememizi sağlar.

Veri seti üzerinde gerekli preprocessing adımları uyguladım, transaction’lar oluşturdum ve Apriori algorithm kullanılarak frequent itemset’ler ve association rule’lar çıkardım. Ayrıca farklı support ve confidence değerleri denenerek bu parametrelerin sonuçlar üzerindeki etkisini inceledim.

Not: Kod geliştirme sürecinde yapay zekâ destekli bir araçtan yararlanılmıştır.
Not2: .csv dosyaları data klasörünün içine taşıdım, kodun çalışması için aynısı yapılmalıdır.

## **2. Dataset Description**

Kullanılan veri setindeki tablolar ve açıklamaları:
- orders.csv: Her sipariş için order bilgilerini içerir. Örneğin order_id, order_dow ve order_hour_of_day.

- order_products.csv: 
Hangi order içinde hangi product’ların bulunduğunu gösterir.

- products.csv: 
Product isimlerini ve product kategorilerini içerir.

- aisles.csv: 
Product’ları aisle kategorileri ile eşleştirir.

- departments.csv: 
Daha genel product kategorilerini içerir.

Orijinal veri seti yaklaşık 3.4 milyon order içermekte. Association rule mining algoritmaları büyük veri setlerinde oldukça maliyetli olduğu için analizde 50,000 order’lık rastgele bir sample kullandım.

```python
sample_size = 50000

sampled_orders = orders.sample(n=sample_size, random_state=42)
```

## **3. Data Preparation**

Analizde her order bir transaction olarak kabul edilmiştir.

Item olarak doğrudan `product_id` kullanmak yerine `aisle` kategorileri kullandım. aisle kategorileri daha yorumlanabilir ve asile'yi kullanmak item sayısını azaltarak analizi daha yönetilebilir hale getiriyor.

Data preparation sürecinde şu adımları uyguladım:

1. orders tablosundan rastgele 50,000 order sample aldım.

2. order_products tablosunu yalnızca bu order’lara ait kayıtları içerecek şekilde filtreledim.

3. Product bilgilerini products tablosundan ekledim.

4. Aisle kategorileri aisles tablosu ile join ettim.

5. Her order_id için transaction oluşturmak amacıyla verileri group ettim.

6. Aynı transaction içinde tekrar eden aisle değerleri kaldırdım.

7. Bu işlemler sonucunda her transaction'ı bir order içindeki benzersiz aisle kategorilerinden oluşan bir liste haline getirdim.

Bu işlemler sonucu oluşan tablodan bir örnek:

```
393 -> [breakfast bars pastries, candy chocolate, fresh fruits, milk, packaged cheese, packaged produce]

```

## **4. Frequent Itemset Mining**

Frequent itemset’leri bulmak için `Apriori` algorithm kullandım.

Apriori algoritmasını uygulayabilmek için transaction verileri önce one-hot encoded formata dönüştürdüm. Bu işlem için TransactionEncoder kullandım. Bu formatta her sütun bir aisle kategorisini temsil eder ve her transaction için bu kategorinin bulunup bulunmadığını gösteren binary değerler içerir.

Daha sonra Apriori algorithm kullanılarak minimum support değerini geçen itemset’ler bulunmuştur.

## **5. Threshold Analysis**

Association rule mining sonuçları seçilen support ve confidence değerlerine oldukça duyarlıdır. Bu nedenle farklı threshold değerleri denenerek sonuçların nasıl değiştiğini inceledim.

Support değeri azaltıldığında bulunan itemset ve rule sayısının hızla arttığını gördüm.

| min_support | frequent itemsets | rules |
|-------------|-------------------|-------|
| 0.02        | 420               | 266   |
| 0.01        | 930               | 378   |
| 0.005       | 1747              | 459   |

Benzer şekilde confidence değeri arttıkça rule sayısı azalmaktadır.

| min_support | rules |
|-------------|-------|
| 0.2         | 9753  |
| 0.3         | 6796  |
| 0.5         | 3647  |
| 0.7         | 1598  |

Daha yüksek confidence değerleri daha güvenilir rule’lar üretirken toplam rule sayısını azaltır.

## **6. Association Rules and Insights**

Apriori analizi sonucunda birkaç anlamlı association rule elde ettim.

### **Rule 1**

**pasta sauce → dry pasta**

- support: 0.0196

- confidence: 0.3139

- lift: 4.45

Bu rule yüksek lift değerine sahiptir ve güçlü bir tamamlayıcı ürün ilişkisini göstermektedir. Pasta sauce satın alan müşterilerin dry pasta satın alma olasılığı ortalamadan çok daha yüksektir. cross-selling stratejileri için kullanılabilir.

### **Rule 2**

**granola → yogurt**

- support: 0.0157

- confidence: 0.5499
- 
- lift: 2.10

Bu rule granola ve yogurt ürünlerinin sıklıkla birlikte satın alındığını göstermektedir. Confidence değerinin yüksek olması granola satın alan müşterilerin yaklaşık yarısının yogurt da satın aldığını göstermektedir. Bu durum özellikle kahvaltı veya sağlıklı atıştırmalık tüketim alışkanlıklarını yansıtıyor olabilir.

### **Rule 3**

**fresh herbs → fresh vegetables**

- support: 0.0778

- confidence: 0.8399
  
- lift: 1.89

Bu rule oldukça yüksek bir confidence değerine sahiptir. Fresh herbs satın alan müşterilerin büyük çoğunluğu aynı zamanda fresh vegetables da satın almaktadır. Bu durum müşterilerin yemek hazırlamak için bu ürünleri birlikte satın aldığını göstermektedir.

### **Rule 4**

**fresh fruits → fresh vegetables**

- support: 0.3175

- confidence: 0.5709
  
- lift: 1.28

Bu rule en yüksek support değerine sahip kurallardan biridir. Bu da müşterilerin alışverişlerinde meyve ve sebze kategorilerini sıklıkla birlikte satın aldığını göstermektedir. Lift değeri çok yüksek olmasa da yüksek support değeri bu ilişkinin oldukça yaygın bir alışveriş davranışı olduğunu göstermektedir.


## **7. Time-based Pattern Analysis**

Product kategorileri arasındaki ilişkilerin yanında alışveriş zamanının da transaction davranışları üzerinde etkili olup olmadığını inceledim. Bu amaçla her transaction’a siparişin verildiği zaman dilimi de bir item olarak eklenmiştir.

`order_hour_of_day` değişkeni daha anlamlı analiz yapabilmek için dört zaman kategorisine ayrılmıştır:

- morning

- afternoon

- evening

- night

Bu işlemden sonra transaction listeleri hem product kategorilerini hem de alışveriş zamanını içerecek şekilde yeniden oluşturdum. Örnek bir transaction:

```
[fresh fruits, yogurt, milk, morning]
```

Apriori algoritması tekrar çalıştırıldığında bazı rule’ların belirli zaman dilimleri ile birlikte ortaya çıktığını gördüm. Örneğin aşağıdaki rule dikkat çekici:

Rule: 
```
{pasta sauce, afternoon} → {dry pasta}

- support: 0.0106
- confidence: 0.3333
- lift: 4.73
```

Bu rule yüksek bir lift değerine sahiptir. Bu sonuç, öğleden sonra pasta sauce alan müşterilerin dry pasta alma olasılığının daha yüksek olduğunu göstermektedir. Bu durum müşterilerin yemek hazırlığı için alışveriş yapması ile açıklanabilir.

Ayrıca bazı rule’larda afternoon zamanının fresh vegetables ve packaged cheese gibi ürünlerle birlikte ortaya çıktığı görülmüştür. Bu da müşterilerin bu saatlerde yemek için gerekli ürünleri birlikte satın alma eğiliminde olduğunu göstermektedir.

Bu sonuçlar alışveriş zamanının da müşteri davranışını etkileyebileceğini göstermektedir. Bu tür bilgiler time-aware recommendation systems için faydalı olabilir.


## **8. Conclusion**

Bu çalışmada grocery transaction verileri üzerinde association rule mining uyguladım. Apriori algorithm kullanılarak birlikte sık satın alınan product kategorileri belirledim.

Elde edilen rule’lar müşterilerin alışveriş davranışları hakkında anlamlı bilgiler gösteriyor. Özellikle bazı ürün kategorilerinin birlikte satın alınma eğilimi açık şekilde görülmüştür. Ayrıca yapılan kısa time-based analiz, alışveriş zamanının da bazı ürün kombinasyonları ile ilişkili olabileceğini göstermiştir.

Bu tür analizler mağaza yerleşimi, cross-selling stratejileri ve recommendation systems geliştirmek için faydalı olabilir.
