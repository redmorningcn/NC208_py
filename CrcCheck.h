
#ifndef  _CrcCheck_h_
#define  _CrcCheck_h_

//----------------------------------------------------------------------------
// ��    �ƣ�   unsigned short GetCrc16Check(uint8 *Buf, unsigned short Len)
// ��    �ܣ�   ȡCRC16У���
// ��ڲ�����  
// ���ڲ�����   
//----------------------------------------------------------------------------
extern	unsigned short GetCrc16Check(unsigned char *Buf, unsigned short Len);
    
extern	unsigned short GetModBusCrc16(unsigned char *puchMsg,unsigned short  usDataLen);    

extern	unsigned short GetModBusCrc16Up(unsigned char *puchMsg,unsigned short  usDataLen);

extern	unsigned char GetCheckSum(unsigned char  Buf[], unsigned int Len);

extern	unsigned char GetCheckSumNR(unsigned char  Buf[], unsigned int Len); 

extern	uint64_t GetCrc32Chk(uint64_t m_CRC, uint8_t  *buf, uint16_t len);
#endif


