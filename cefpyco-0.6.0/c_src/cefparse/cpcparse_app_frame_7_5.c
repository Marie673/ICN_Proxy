/*
 * Copyright (c) 2016, National Institute of Information and Communications
 * Technology (NICT). All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the NICT nor the names of its contributors may be
 *    used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE NICT AND CONTRIBUTORS "AS IS" AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE NICT OR CONTRIBUTORS BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>
#include <ctype.h>

#include "cefpyco_util.h"
#include "cpcparse_type.h"
#include "cpcparse_tlv.h"
#include "cpcparse_app_frame_7_5.h"

static int is_not_ccnx_1_0_content_packet(unsigned char *buf, int len);
static int is_not_targeted_header(struct cef_app_frame* wrk_frame);
    
int cpcparse_try_parse_app_frame_7_5(
    cpcparse_parse_info* info,
    cefpyco_app_frame* app_frame)
{        
    int res;
    int actual_len;
    struct cef_app_frame *wrk_buf = &(info->wrk_frame);
    unsigned char *buf = info->buf;
    int remained_length = info->len - info->offset;
MILESTONE

    if (is_not_ccnx_1_0_content_packet(buf, remained_length)) { return 0; } 
    memset(wrk_buf, 0, sizeof(struct cef_app_frame));
    res = cef_client_payload_get_with_info(buf, remained_length, wrk_buf);
    if (res < 0) { return 0; }
    if (is_not_targeted_header(wrk_buf)) { return 0; }
    
    actual_len = info->len - info->offset - res;
    if(info->offset + actual_len > info->len) { return -1; } // Too short body
    
    app_frame->version = wrk_buf->version;
    app_frame->type = CPC_CCNX_PT_CONTENT;
    app_frame->flags = 0x00000000ul;
    app_frame->actual_data_len = actual_len;
    app_frame->name = wrk_buf->name;
    app_frame->name_len = wrk_buf->name_len;
    app_frame->chunk_num = wrk_buf->chunk_num;
    app_frame->end_chunk_num = wrk_buf->end_chunk_num;
    app_frame->payload = wrk_buf->payload;
    app_frame->payload_len = wrk_buf->payload_len;
    return actual_len;
}

static int is_not_ccnx_1_0_content_packet(unsigned char *buf, int len) {
    if (len < 2) return 1;
    return 
        (buf[0] != CPC_CCNX_VERSION) ||
        (buf[1] != CPC_CCNX_PT_CONTENT);
}

static int is_not_targeted_header(struct cef_app_frame* wrk_buf) {
    return 
        (wrk_buf->version != CefC_App_Version) || 
        (wrk_buf->type != CefC_App_Type_Internal);
}
