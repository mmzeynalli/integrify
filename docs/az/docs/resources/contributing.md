# Development - Contributing

İlk öncə (və ən rahat), proyekti ulduzlayaraq yardımçı ola bilərsiniz.

## Issue

[Githubda](https://github.com/mmzeynalli/integrify/issues) yeni issue açaraq, yeni feature təklif edə, və ya mövcud bugları qeyd edə bilərsiniz.
Bug qeyd etdikdə, istifadə etdiyiniz əməliyyat sistemi və kitabxananın versiyasını qeyd etməyiniz tövsiyyə olunur.

## Development

Əgər [integrify repo-sunu](https://github.com/mmzeynalli/integrify/) artıq klonlamısınızsa, növbəti mərhələləri izləyərək öz kodunuzu əlavə edə bilərsiniz. Contribution sadə və sürətli olsun deyə test və linting-i lokal mühitinizdə icra etməyiniz məsləhət görülür. Integrify-ın başqa kitabxanalardan çox az asılılığı olduğundan quraşdırılma çox sadədir.

!!! tip

    **tl;dr:** Kodu format etmək üçün `make format`, test və lint etmək üçün `make` və dokumentasiya generasiya etmək üçün `make docs` kommandını icra edin.

### Rekvizitlər { #requisites }

* Python 3.9 və 3.12 arası istənilən versiya
* git
* make
* [Poetry](https://python-poetry.org/docs/#installation)

### İnstallasiya və quraşdırılma  { #installation }

```bash
# Proyekti klonlayın və həmin qovluğa keçin
git clone git@github.com:<your username>/integrify.git
cd integrify

# Poetry yükləyin (https://python-poetry.org/docs/#installation)
curl -sSL https://install.python-poetry.org | python3 -

# Bütün dependency-ləri yükləyin
make install
```

### Yeni branch-a keçin və öz dəyişiklikləriniz əlavə edin  { #new-branch }

```bash
# Yeni branch-a keçid edin
git checkout -b my-new-feature-branch
# Öz dəyişikliklərini əlavə edin...
```

???+ warning

    Branch adını uyğun seçin:

    * Bug düzəldirsizsə, `bug/branch-name`
    * Yeni inteqrasiya əlavə edirsizsə, `integration/integration-name`
    * Kiçik fix-dirsə: `fix/branch-name`
    * Dokumentasiya üzərində işləyirsinizsə: `docs/branch-name`

### Test və Linting

Kod dəyişiklikləriniz etdikdən sonra lokalda testləri və lintingi işə salın:

```bash
make format
# Integrify Rust-da yazılmış ruff Python linterini istifadə edir
# https://github.com/astral-sh/ruff

make
# Bu kommand öz içində bir neçə başqa kommandı icra edir (`test` və `lint`)
```

### Yeni dokumentasiyanı generasiya edin

Əgər dokumentasiyada (və ya funksiyalarda, klass definitionlarında və ya docstring-lərdə) dəyişiklik etmisinizsə, yeni dokumentasiya generasiya edin.
Dokumentasiya üçün `mkdocs-material` alətindən istifadə edirik.

```bash
# Dokumentasiya generasiya edin
make docs
# Əgər dokumentasiyaya təsir edəcək kod dəyişikliyi etmisinizsə, 
# əmin olun ki, yeni dokumentasiya uğurlar generasiya olunur.

# make docs-serve kommandını icra etsəz, localhost:8000 addresində yeni dokumentasiyanı da görə bilərsiniz.
```

### Dəyişiklikləriniz commit və push edin  { #commit-push-and-pr }

Dəyişikliklərinizi bitirdək sonra, commit və öz branch-ınıza push edib, bizə pull request yaradın.

Pull request-iniz review üçün hazırdırsa, "Zəhmət olmazsa, review edin" comment-ini yazın, ən yaxın zamanda nəzər yetirəcəyik.

## Kod arxitekturası (!) { #code-architecture }

Bu hissə uzun və detallı yazılmalı olduğundan, məqalə [burada](./code-architecture.md) yerləşdirilib.

## Dokumentasiya stili { #documentation }

Dokumentasiya markdown-da yazılır və [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) aləti ilə generasiya olunur. API dokumentasiyası isə docstring-lərdən [mkdocstrings](https://mkdocstrings.github.io/) ilə generasiya olunur.

### Kodun dokumentləşdirilməsi { #incode-documentation-style }

Öz dəyişikliklərinizi əlavə edərkən, bütün kodun dokumentləşdirildiyindən əmin olun. Qeyd olunanlar format olunmuş docstring-lərlə yaxşıca dokumentləşdirilməlidir:

* Modullar
* Klass definition-ları
* Funksiya definition-ları
* Module səviyyəsində dəyişənlər

Integrify [PEP 257](https://www.python.org/dev/peps/pep-0257/) standartları ilə format olunmuş [Google-style docstring-lərdən](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)  istifadə edir. (Əlavə məlumat üçün [Example Google Style Python Docstrings-ə](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) baxın.)

Docstring-lərdə misal (example) göstərə bilərsiniz. Bu misal tam işlənə bilən kod olmalıdır.

### Dokumentasiya { #documentation-style }

Ümumiyyətlə, dokumentasiya əlçatan üslubda yazılmalıdır. Oxunması və başa düşülməsi asan olmalı, qısa və konkret olmalıdır.

Kod nümunələri əlavə etməyiniz şiddətlə tövsiyyə olunur, lakin qısa və sadə saxlanılmalıdır. Bununla belə, hər bir kod nümunəsi tam, müstəqil və işlək olmalıdır. (Bunu necə edəcəyinizə əmin deyilsinizsə, kömək istəyin!).

## Tərcümə { #translation }

Hal-hazırda proyekt əsasən Azərbaycanlı developerlər üçün nəzərdə tutulduğundan, dokumentasiya və docstring-lər Azərbaycan dilindədir.
Amma, bu proyekti gələcəkdə daha qloballaşdırmaq fikrində olduğumuzdan, ingiliscəyə tərcümədə yardıma ehtiyacımız var. Gələcəkdə ölkə-spesifik inteqrasiyalar
mövcud olduqda, həmin dillərə də ehtiyac duyacağıq.
