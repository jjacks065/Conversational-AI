WITH CTECLAIMS AS
(SELECT 
    CLCL.CLCL_ID                                                    AS CLAIM_NUMBER, 
    CLCL.CLCL_CL_TYPE                                               AS CLAIM_TYPE_CD,
    CLCL.PRPR_ID                                                    AS PROVIDER_ID,
    PRPR.PRPR_NAME                                                  AS PROVIDER_NAME,
    CLCL.CLCL_TOT_CHG                                               AS BILL_AMT,  
    TO_CHAR(CLCL.CLCL_ACPT_DTM,'MM/dd/YYYY')                        AS CLAIM_PROCESSED_DT, 
    TO_CHAR(CLCL.CLCL_RECD_DT ,'MM/dd/YYYY')                        AS CLAIM_RECEIVED_DT,      								 	
    --TO_CHAR(CLCL.CLCL_LAST_ACT_DTM ,'hh:mi a.m., MM/dd/yyyy' )    AS CLAIM_LAST_UP_DATE, 
    TO_CHAR(CLCL_HIGH_SVC_DT,'MM/dd/yyyy' )             AS CLAIM_LAST_UP_DATE, --Modified
    CASE
            WHEN CLCL.CLCL_CL_TYPE IN ('M','E')
            THEN (SELECT SUM(CDML_TOT_PA_LIAB) FROM FC_CMC_CDML_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID)
            ELSE (SELECT SUM(CDDL_TOT_PA_LIAB) FROM FC_CMC_CDDL_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID)
    END                                                             AS PA_RESP_AMT,	--   field name "Patient Liability Disallow" in claims inquiry 
    CASE
            WHEN CLCL.CLCL_CL_TYPE IN ('M','E')
            THEN (SELECT SUM(CDML_ALLOW) FROM FC_CMC_CDML_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID)
            ELSE (SELECT SUM(CDDL_ALLOW) FROM FC_CMC_CDDL_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID)
    END                                                             AS ALLOWED_AMT,	
    CASE
            WHEN CLCL.CLCL_CL_TYPE IN ('M','E')
            THEN (SELECT SUM(CDML_DED_AMT) FROM FC_CMC_CDML_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID)
            ELSE (SELECT SUM(CDDL_DED_AMT) FROM FC_CMC_CDDL_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID)
    END                                                             AS DED_AMT,												
    CASE
            WHEN CLCL.CLCL_CL_TYPE IN ('M','E')
            THEN (SELECT SUM(CDML_COPAY_AMT) FROM FC_CMC_CDML_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID)
            ELSE (SELECT SUM(CDDL_COPAY_AMT) FROM FC_CMC_CDDL_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID)
    END                                                             AS COPAY_AMT,											
    CASE
            WHEN CLCL.CLCL_CL_TYPE IN ('M','E')
            THEN (SELECT SUM(CDML_COINS_AMT) FROM FC_CMC_CDML_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID)
            ELSE (SELECT SUM(CDDL_COINS_AMT) FROM FC_CMC_CDDL_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID)
    END                                                             AS COINS_AMT,											
    (CASE
		    WHEN CLCL.CLCL_CL_TYPE IN ('M','E')
		    THEN
		      -- Obtain status for medical claims
		      CASE
		        WHEN CLCL.CLCL_CUR_STS = '02'
		        THEN
		          CASE
		            WHEN (SELECT SUM(CDML_CONSIDER_CHG) FROM FC_CMC_CDML_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) > 0
		            AND (SELECT SUM(CDML_ALLOW) FROM FC_CMC_CDML_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) = 0
		            AND TRIM(CLCL.CLCL_ID_ADJ_FROM) IS NOT NULL
		            THEN 'FINALIZED - DENIED (ADJUSTED)'
		            WHEN (SELECT SUM(CDML_CONSIDER_CHG) FROM FC_CMC_CDML_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) >0
		            AND (SELECT SUM(CDML_ALLOW) FROM FC_CMC_CDML_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) = 0
		            THEN 'FINALIZED - DENIED'
		            WHEN TRIM(CLCL.CLCL_ID_ADJ_FROM) IS NOT NULL
		            THEN 'FINALIZED ADJUSTED'
		            ELSE 'FINALIZED'
		          END
		        WHEN CLCL.CLCL_CUR_STS = '91'
		        THEN
		          CASE
		            WHEN (SELECT SUM(CDML_CONSIDER_CHG) FROM FC_CMC_CDML_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) > 0
		            AND (SELECT SUM(CDML_ALLOW) FROM FC_CMC_CDML_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) = 0
		            THEN 'FINALIZED - DENIED (ADJUSTED)'
		            ELSE 'FINALIZED ADJUSTED'
		          END
		        WHEN CLCL.CLCL_CUR_STS NOT IN ('91', '02')
		        THEN
		          CASE
		            WHEN TRIM(CLCL.CLCL_ID_ADJ_FROM) IS NOT NULL
		            THEN 'IN PROCESS (ADJUSTED)'
		            ELSE 'IN PROCESS'
		          END
		        ELSE 'IN PROCESS'
		      END
		    ELSE
            -- Obtain status for dental claims
            CASE
		        WHEN CLCL.CLCL_CUR_STS = '02'
		        THEN
		          CASE
		            WHEN (SELECT SUM(CDDL_CONSIDER_CHG) FROM FC_CMC_CDDL_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) > 0
		            AND (SELECT SUM(CDDL_ALLOW)  FROM FC_CMC_CDDL_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) = 0
		            AND TRIM(CLCL.CLCL_ID_ADJ_FROM) IS NOT NULL
		            THEN 'FINALIZED - DENIED (ADJUSTED)'
		            WHEN (SELECT SUM(CDDL_CONSIDER_CHG) FROM FC_CMC_CDDL_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) > 0
		            AND (SELECT SUM(CDDL_ALLOW)  FROM FC_CMC_CDDL_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) = 0
		            THEN 'FINALIZED - DENIED'
		            WHEN TRIM(CLCL.CLCL_ID_ADJ_FROM) IS NOT NULL
		            THEN 'FINALIZED ADJUSTED'
		            ELSE 'FINALIZED'
		          END
		        WHEN CLCL.CLCL_CUR_STS = '91'
		        THEN
		          CASE
		            WHEN (SELECT SUM(CDDL_CONSIDER_CHG) FROM FC_CMC_CDDL_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) > 0
		            AND (SELECT SUM(CDDL_ALLOW)  FROM FC_CMC_CDDL_CL_LINE WHERE CLCL_ID = CLCL.CLCL_ID) = 0
		            THEN 'FINALIZED - DENIED (ADJUSTED)'
		            ELSE 'FINALIZED ADJUSTED'
		          END
		        WHEN CLCL.CLCL_CUR_STS NOT IN ('91', '02')
		        THEN
		          CASE
		            WHEN TRIM(CLCL.CLCL_ID_ADJ_FROM) IS NOT NULL
		            THEN 'IN PROCESS (ADJUSTED)'
		            ELSE 'IN PROCESS'
		          END
		        ELSE 'IN PROCESS'
		      END
     END)           										        AS CLAIM_STATUS,									
    (SELECT 
            CDML_DISALL_EXCD 
    FROM FC_CMC_CDML_CL_LINE WHERE ROWNUM = 1 
    AND CLCL_ID = CLCL.CLCL_ID)                                     AS DENIAL_CODE,   --field name "Disallow explanation" in claims inquiry
    CASE
            WHEN CLCL.CLCL_PRE_PRICE_IND IN ('E','H','I','T','S')
            THEN 'true'
            ELSE 'false'
    END 															AS ITS_CLAIM,
    CLCL.CLCL_EOB_EXCD_ID                                           AS CLAIM_EXCD_ID, --Modified
    CASE
            WHEN (EXISTS(SELECT 1 FROM FC_CMC_PDDS_PROD_DESC WHERE PDPD_ID = CLCL.PDPD_ID 
                         AND PDDS_DESC LIKE '%FEP%') AND CLCL.CLCL_CL_TYPE = 'D')
            THEN 'true'
            ELSE 'false'
    END 	                                                        AS FEP_DENTAL_CLAIM,								
    TO_CHAR(CLCL.CLCL_LOW_SVC_DT,'MM/dd/YYYY')                      AS CLM_DT_OF_SERVICE,								
    CASE
            WHEN CLCL.CLCL_PRE_PRICE_IND IN ('S', 'E', 'I')
            THEN CLIP.CLIP_FIRST_NAME
            ELSE MEME.MEME_FIRST_NAME
    END 															AS MEM_FIRST_NAME,									
    CASE
            WHEN CLCL.CLCL_PRE_PRICE_IND IN ('S', 'E', 'I')
            THEN TO_CHAR(CLIP.CLIP_BIRTH_DT ,'MM/dd/YYYY')
            ELSE TO_CHAR(MEME.MEME_BIRTH_DT ,'MM/dd/YYYY')
  	END 															AS MEM_BIRTH_DT,									
	SBSB.SBSB_ID                                                    AS SUB_ID,
    LPAD(MEME.MEME_SFX, 2, 0)                                       AS SUFFIX,
    CLCL.CLCL_CUR_STS                                               AS CLAIM_STATUS_CODE,                                                                                                                           
    PRPR.PRPR_NPI                                                   AS PROVIDER_NPI,
    PRPR.MCTN_ID                                                    AS PROVIDER_TAXID
    FROM FC_CMC_CLCL_CLAIM CLCL
    INNER JOIN FACETS.CMC_MEME_MEMBER MEME
    ON CLCL.MEME_CK = MEME.MEME_CK
    INNER JOIN FC_CMC_PRPR_PROV PRPR
    ON CLCL.PRPR_ID = PRPR.PRPR_ID
    LEFT JOIN FC_CMC_CLIP_ITS_PATNT CLIP
    ON CLCL.CLCL_ID = CLIP.CLCL_ID
    INNER JOIN (
    (SELECT 
        NULL AS CLCL_ID,
        SBSB_CK AS SBSB_CK,
        SBSB_ID AS SBSB_ID
    FROM
        FC_CMC_SBSB_SUBSC 
    WHERE SBSB_ID = TO_CHAR(:subscriberId))
    UNION
    (SELECT
        CLCL_ID AS CLCL_ID,
        NULL AS SBSB_CK,
        CLMI_ITS_SBSB_ID AS SBSB_ID
    FROM FC_CMC_CLMI_MISC  
    WHERE CLMI_ITS_SBSB_ID = TO_CHAR(:subscriberId))
    ) SBSB
    ON ((CLCL.CLCL_ID = SBSB.CLCL_ID AND CLCL.CLCL_PRE_PRICE_IND IN ('S', 'E', 'I')) 
         OR (CLCL.CLCL_PRE_PRICE_IND NOT IN ('S', 'E', 'I') AND CLCL.SBSB_CK = SBSB.SBSB_CK))
    --DYNAMIC CONTENT APPEND 1--
    --WHERE LPAD(MEME.MEME_SFX, 2, 0) = :memberSuffix
    --DYNAMIC CONTENT APPEND 1--
    --AND PRPR.PRPR_NPI = (:providerNpi)
    --AND PRPR.MCTN_ID = (:providerTaxId)
    --AND CLCL.CLCL_TOT_CHG BETWEEN (:billedAmountFrom) AND (:billedAmountTo)
    AND CLCL.CLCL_LOW_SVC_DT BETWEEN TO_DATE(:dateOfServicesFrom, 'YYYY-MM-DD') AND TO_DATE(:dateOfServicesTo, 'YYYY-MM-DD')
    AND (CLCL.CLCL_CUR_STS IS NULL OR CLCL.CLCL_CUR_STS <> '81')
)
SELECT DISTINCT  
       CTE.CLAIM_NUMBER,
       CTE.CLAIM_TYPE_CD,
       CTE.PROVIDER_ID,											
       CTE.PROVIDER_NAME,
       CTE.BILL_AMT,                                                
       CTE.CLAIM_PROCESSED_DT,
       CLCK.CLCK_NET_AMT                                            AS TOT_PAID_AMT,       									
       CTE.CLAIM_RECEIVED_DT,      								 	
       CTE.CLAIM_LAST_UP_DATE,
       TO_CHAR(CKCK.CKCK_PRINTED_DT, 'MM/dd/YYYY')                  AS CHK_EFT_DT,
       BPID.CKPY_NET_AMT                                            AS CHK_EFT_AMT,		--Modified
       NVL(DECODE(CKCK.CKCK_CK_NO, 0, CKCK.CKPY_REF_ID, 
       CKCK.CKCK_CK_NO), BPCL.CKPY_REF_ID)                          AS CHECK_EFT_INFO,				
       CTE.PA_RESP_AMT,											           
       CTE.ALLOWED_AMT,											
       CTE.DED_AMT,												
       CTE.COPAY_AMT,											
       CTE.COINS_AMT,											
       (SELECT 
            CKPY_REF_ID    ||
            CASE
                  WHEN EFT_FLAG = 1
                  THEN NVL(MAX_BPID_SEQ_NO_EFT, MAX_BPID_SEQ_NO)
                  ELSE MAX_BPID_SEQ_NO
            END AS EOB_NUMBER
        FROM
        (
            SELECT BPID2.SYIN_INST,
            BPID2.CKPY_REF_ID,
            MAX(
                CASE
                    WHEN BPID2.BPID_TYPE IN ('ECPR', 'EPPR', 'EPRA', 'PEFT', 'PRCC', 'PRCK', 'XPRP', 'ZCPR',
                    'ZPPR', 'HPCK', 'HPZP', 'LPCK', 'LPZP', 'LSCK', 'LSZP', 'ECPT','SBCK','EOSB' ) --Modified EOSB
                    AND TRIM(BPID2.BPID_PYEE_ACCT_NO)  IS NOT NULL
                    AND TRIM(BPID2.BPID_PYEE_BNK_RTNG) IS NOT NULL
                THEN 1
                ELSE 0
                END ) AS EFT_FLAG,
                MAX(
                  CASE
                        WHEN BPID2.BPID_TYPE IN ('ECPR', 'EPPR', 'EPRA', 'PEFT', 'PRCC', 'PRCK', 'XPRP', 
                        'ZCPR', 'ZPPR', 'HPCK', 'HPZP', 'LPCK', 'LPZP', 'LSCK', 'LSZP', 'ECPT','SBCK','EOSB' ) --Modified EOSB
                        THEN BPID2.BPID_SEQ_NO
                  END )                                                       AS MAX_BPID_SEQ_NO_EFT,
                  MAX(BPID2.BPID_SEQ_NO)                                      AS MAX_BPID_SEQ_NO,
                  MAX(BPID2.SYIN_INST) OVER( PARTITION BY BPID2.CKPY_REF_ID ) AS MAX_SYIN_INST
                  FROM FC_CMC_BPID_INDIC BPID2
                  WHERE BPID2.CKPY_REF_ID = BPCL.CKPY_REF_ID
                  GROUP BY BPID2.SYIN_INST,BPID2.CKPY_REF_ID
                )
              WHERE SYIN_INST = MAX_SYIN_INST
       )                                                                       AS EOB_NUMBER,	
       TO_CHAR(BPID.BPID_PRINTED_DT, 'MM/dd/YYYY')                            AS EOB_ISSUE_DT, --Modified
       CTE.CLAIM_STATUS,									
       CTE.DENIAL_CODE,	
       CKCK.CKCK_CURR_STS                                                      AS CHK_STATUS_CODE,
       (SELECT COUNT(*)
       FROM FC_NWX_WWMS_WARNMSG WWMS
       JOIN FC_CMC_CLCL_CLAIM CLCL2
       ON CLCL2.CLCL_ID          = WWMS.WWMS_MESSAGE_ID
       AND CLCL2.CLCL_ID         = CTE.CLAIM_NUMBER
       WHERE WWMS.WRTR_REASON_ID = '709')                                      AS CLAIM_REASON_ID_COUNT,
       (SELECT MCTR_DESC from FC_CMC_MCTR_CD_TRANS  
        WHERE MCTR_VALUE = CKCK.CKCK_CURR_STS AND MCTR_ENTITY = '^C41' 
        AND MCTR_TYPE ='CSTS')                                                 AS PAYMENT_CHECK_STATUS_SHRT_DESC,
       (CASE WHEN EXISTS
        (SELECT CKPY_REF_ID FROM FC_CMC_CLCK_CLM_CHECK  
        WHERE CKPY_REF_ID = CKCK.CKPY_REF_ID GROUP BY CKPY_REF_ID 
        HAVING COUNT(1) >1) THEN 'Y' ELSE 'N' END)                             AS PAYMENT_SUMMARY_CHECK_IND,						
       --Need Value or Description
       CLCK.CLCK_PAYEE_IND											           AS PAYEE_TYPE,		  	
       -- query for ITS Claim
       CTE.ITS_CLAIM,	
       CTE.CLAIM_EXCD_ID,								
       CTE.FEP_DENTAL_CLAIM,								
       CTE.CLM_DT_OF_SERVICE,								
       CTE.MEM_FIRST_NAME,									
       CTE.MEM_BIRTH_DT,									
	   CTE.SUB_ID,
       CTE.SUFFIX,
       SUBSTR(BPID.PYBA_ID,-4)                                                  AS CLM_CHECK_ACCNO, -- Modified
       CTE.CLAIM_STATUS_CODE,   
       CKCK.CKCK_PAYEE_NAME                                                     AS CHK_PAYEE_NAME,                                                                                                                            
       CTE.PROVIDER_NPI,
       CTE.PROVIDER_TAXID  
FROM CTECLAIMS CTE
LEFT JOIN FC_CMC_BPCL_CLM BPCL
ON CTE.CLAIM_NUMBER = BPCL.CLCL_ID
LEFT JOIN FC_CMC_BPID_INDIC BPID
ON BPCL.CKPY_REF_ID = BPID.CKPY_REF_ID
AND BPCL.CLCL_ID = BPID.CLCL_ID
AND BPID.BPID_TYPE IN ( 'ECPR', 'EPPR','EPRA', 'PEFT', 'PRCC', 'PRCK','XPRP', 'ZCPR', 
'ZPPR', 'HPCK', 'HPZP', 'LPCK', 'LPZP', 'LSCK', 'LSZP', 'ECPT','SBCK','EOSB' ) --Modified EOSB
LEFT JOIN FC_CMC_CLCK_CLM_CHECK CLCK
ON CLCK.CLCL_ID = CTE.CLAIM_NUMBER
AND BPCL.CLCL_ID = CLCK.CLCL_ID
AND BPCL.CKPY_REF_ID = CLCK.CKPY_REF_ID
LEFT JOIN FC_CMC_CKCK_CHECK CKCK
ON CLCK.CKPY_REF_ID = CKCK.CKPY_REF_ID
--DYNAMIC CONTENT APPEND 2--
--WHERE CTE.MEM_FIRST_NAME = 'STEWEN'
--AND CTE.MEM_BIRTH_DT = '01/01/1970' /*MM/dd/YYYY*/;
