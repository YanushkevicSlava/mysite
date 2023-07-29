select "shopapp_product"."id",
       "shopapp_product"."name",
       "shopapp_product"."description",
       "shopapp_product"."price",
       "shopapp_product"."discount",
       "shopapp_product"."created_at",
       "shopapp_product"."archived",
       "shopapp_product"."preview"
       from "shopapp_product"
       where not "shopapp_product"."archived"; args=();
       alias=default

select "shopapp_productimage"."id",
       "shopapp_productimage"."product_id",
       "shopapp_productimage"."image",
       "shopapp_productimage"."description"
       FROM "shopapp_productimage"
       WHERE "shopapp_productimage"."product_id" = 1;
select "shopapp_productimage"."id",
       "shopapp_productimage"."product_id",
       "shopapp_productimage"."image",
       "shopapp_productimage"."description"
       FROM "shopapp_productimage"
       WHERE "shopapp_productimage"."product_id" = 1;
